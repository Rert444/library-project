import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, status
from app.api.deps import SessionDep, CurrentUserDep
from app.repositories.attachment import AttachmentRepository
from app.schemas.attachment import AttachmentRead
from app.core.tasks import log_file_upload

router = APIRouter(prefix="/attachments", tags=["attachments"])

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
FORBIDDEN_EXTENSIONS = {".exe", ".bat", ".sh", ".cmd"}


@router.post("/books/{book_id}", response_model=AttachmentRead, status_code=status.HTTP_201_CREATED)
async def upload_attachment(
        book_id: int,
        session: SessionDep,
        current_user: CurrentUserDep,
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...)
):
    # 1. Проверка расширения
    ext = os.path.splitext(file.filename)[1].lower()
    if ext in FORBIDDEN_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Forbidden file extension")

    # 2. Проверка размера (читаем файл и проверяем)
    file.file.seek(0, 2)  # В конец файла
    file_size = file.file.tell()
    file.file.seek(0)  # Возвращаемся в начало

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    # 3. Сохранение файла
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 4. Сохранение метаданных в БД
    repo = AttachmentRepository(session)
    attachment = await repo.create(
        filename=file.filename,  # Оригинальное имя
        file_path=file_path,  # Путь на диске
        content_type=file.content_type,
        size=file_size,
        book_id=book_id
    )

    # 5. Запуск фоновой задачи!
    background_tasks.add_task(log_file_upload, filename=file.filename, book_id=book_id)

    return attachment


@router.delete("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attachment(
        attachment_id: int,
        session: SessionDep,
        current_user: CurrentUserDep
):
    repo = AttachmentRepository(session)
    attachment = await repo.get(attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    # Удаляем с диска
    if os.path.exists(attachment.file_path):
        os.remove(attachment.file_path)

    # Удаляем из БД
    await repo.delete(attachment)
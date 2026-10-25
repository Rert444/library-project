from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attachment import Attachment


class AttachmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, filename: str, file_path: str, content_type: str, size: int, book_id: int) -> Attachment:
        attachment = Attachment(
            filename=filename,
            file_path=file_path,
            content_type=content_type,
            size=size,
            book_id=book_id
        )
        self.session.add(attachment)
        await self.session.commit()
        await self.session.refresh(attachment)
        return attachment

    async def get(self, attachment_id: int) -> Attachment | None:
        return await self.session.get(Attachment, attachment_id)

    async def delete(self, attachment: Attachment) -> None:
        await self.session.delete(attachment)
        await self.session.commit()
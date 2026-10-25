import time
import logging

logger = logging.getLogger(__name__)

def log_file_upload(filename: str, book_id: int):
    # Имитация долгой работы (например, отправка уведомления)
    time.sleep(2)
    logger.info(f"ФАЙЛ УСПЕШНО ОБРАБОТАН: {filename} для книги ID={book_id}")
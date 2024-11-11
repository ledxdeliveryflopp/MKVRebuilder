import os

import psutil
from loguru import logger


@logger.catch
def calculate_storage(source_path: str, output_path: str) -> dict:
    """Подсчет хватит ли места на новый файл"""
    try:
        source_file_data = os.stat(source_path)
        source_file_size = source_file_data[6]
        disc_data = psutil.disk_usage(output_path)
        disc_free = round(disc_data.free / (1024 ** 3), 3)
        output_file_size = round(source_file_size / (1024 ** 3), 3) - 12
        return {"disc_free": disc_free, "output_file_size": output_file_size}
    except TypeError as exception:
        logger.info(f"calculate_storage: {exception}")

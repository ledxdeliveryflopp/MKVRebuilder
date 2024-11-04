import subprocess
import sys

from PySide6.QtWidgets import QApplication
from loguru import logger

from src.main.window import MainWindow
from src.settings.config import ini_settings


@logger.catch
def set_up_app() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    logger.add("application.log", rotation="100 MB",
               format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}")
    ini_settings.set_base_ini_config()
    set_up_app()






import os

import psutil
from PySide6 import QtGui
from PySide6.QtCore import QTranslator, QLocale
from PySide6.QtWidgets import QApplication
from loguru import logger

from src.main.window import MainWindow
from src.settings.config import ini_settings


@logger.catch
def set_up_translator() -> QTranslator:
    """Установка перевода"""
    translator = QTranslator()
    system_language = QLocale.system().name()
    if system_language:
        translator.load(f"static/localization/{system_language}.qm")
        logger.info(f"Set lang {system_language}")
    return translator


@logger.catch
def set_up_fonts() -> None:
    app_location = os.path.dirname(os.path.realpath(__file__))
    fonts_location = rf"{app_location}\static\fonts"
    fonts_list = os.listdir(fonts_location)
    for font in fonts_list:
        font_path = rf"{fonts_location}\{font}"
        QtGui.QFontDatabase.addApplicationFont(font_path)
    logger.info(f"Fonts installed")


@logger.catch
def close_all_subprocess() -> None:
    """Завершить все подпроцессы при закрытии приложения"""
    current_process = psutil.Process()
    children_process = current_process.children(recursive=True)
    if children_process:
        for process in children_process:
            process_pid = process.pid
            process = psutil.Process(process_pid)
            process.terminate()
            logger.info(f"Process {process.pid} closed")


@logger.catch
def set_up_app() -> None:
    app = QApplication()
    translator = set_up_translator()
    app.installTranslator(translator)
    set_up_fonts()
    window = MainWindow()
    window.show()
    logger.info("App inited")
    app.exec()
    close_all_subprocess()


if __name__ == '__main__':
    logger.add("application.log", rotation="100 MB",
               format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}")
    ini_settings.set_base_ini_config()
    set_up_app()







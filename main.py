import os
import sys

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
    return translator


@logger.catch
def set_up_fonts() -> None:
    app_location = os.path.dirname(os.path.realpath(__file__))
    fonts_location = rf"{app_location}\static\fonts"
    fonts_list = os.listdir(fonts_location)
    for font in fonts_list:
        font_path = rf"{fonts_location}\{font}"
        QtGui.QFontDatabase.addApplicationFont(font_path)
    font_database = QtGui.QFontDatabase.families(QtGui.QFontDatabase.WritingSystem.Any)
    logger.info(f"font in db: {font_database}")


@logger.catch
def set_up_app() -> None:
    app = QApplication(sys.argv)
    translator = set_up_translator()
    app.installTranslator(translator)
    set_up_fonts()
    QtGui.QFontDatabase.families(QtGui.QFontDatabase.WritingSystem.Any)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    logger.add("application.log", rotation="100 MB",
               format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}")
    ini_settings.set_base_ini_config()
    set_up_app()







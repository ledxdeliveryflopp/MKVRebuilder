from PySide6 import QtWidgets
from loguru import logger

from src.console.widget import ConsoleWidget
from src.rebuilder.widget_ui import UiSettingsWidget


class SettingsWidget(QtWidgets.QWidget):
    """Виджет выбора битрейта и старта конвертации"""

    def __init__(self, main_window: QtWidgets.QMainWindow,
                 source_file: str, output_file: str, track_data: dict, subtitle_data: dict | None, temp_path: str):
        super().__init__()
        self.main_window = main_window
        self.source_file: str = source_file
        self.output_file: str = output_file
        self.track_data: dict = track_data
        self.subtitle_data: dict | None = subtitle_data
        self.temp_path: str = temp_path
        self.bitrate: int = 192
        self.ui = UiSettingsWidget()
        self.ui.setupUi(self)
        self.translate_ui()
        self.set_bitrate_variants()
        self.set_signals()

    @logger.catch
    def translate_ui(self) -> None:
        """Перевод интерфейса"""
        self.ui.bitrate_label.setText(self.tr("Select bitrate"))
        self.ui.start_button.setText(self.tr("Start"))

    @logger.catch
    def set_bitrate_variants(self) -> None:
        """Установка возможных битрейтов"""
        self.ui.bitrate_box.addItem("192")
        self.ui.bitrate_box.addItem("256")
        self.ui.bitrate_box.addItem("384")
        self.ui.bitrate_box.addItem("448")
        self.ui.bitrate_box.addItem("640")

    @logger.catch
    def set_signals(self) -> None:
        """Установка сигналов"""
        self.ui.bitrate_box.currentTextChanged.connect(self.set_bitrate)
        self.ui.start_button.clicked.connect(self.start_rebuild)

    @logger.catch
    def set_bitrate(self, bitrate: str) -> None:
        """Установка битрейта"""
        self.bitrate = int(bitrate)

    @logger.catch
    def start_rebuild(self) -> None:
        """"""

        self.console_widget = ConsoleWidget(self.main_window, self.source_file, self.output_file, self.track_data,
                                            self.subtitle_data, self.temp_path, self.bitrate)
        self.console_widget.show()
        self.close()

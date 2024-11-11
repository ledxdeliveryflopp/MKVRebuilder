from typing import Any
from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QAbstractItemView, QMenuBar, QLabel
from loguru import logger

from src.info.service import mkv_merge_service
from src.main.widget_ui import UiMainWindow
from src.rebuilder.widget import RebuilderWidget

from src.settings.config import ini_settings
from src.settings.settings import settings
from src.settings.thread_manager import DebugThread


class MainWindow(QtWidgets.QMainWindow):
    """Класс основного окна/виджета"""

    def __init__(self) -> None:
        super().__init__()
        self.temp_path: str = ini_settings.get_temp_dir()
        self.output_path: str = ini_settings.get_output_dir()
        self.data_fill_count: int = 0
        self.data_fill_count_dict: dict = {"source": 0, "temp": 0, "output": 0, "sound": 0}
        self.source_file_name: str | None = None

        self.debug_thread: DebugThread = DebugThread(disc="F:")

        self.source_path: str | None = None
        self.output_file: str | None = None

        self.track_data: dict | None = None
        self.subtitle_data: dict | None = None
        self.bitrate: int = 192
        self.restricted_codec: str | None = None

        self.restricted_codec_list: list = ["AC-3", "E-AC-3"]
        self.audio_model = None
        self.subtitle_model = None
        self.rebuilder_widget: QtWidgets = None

        self.black_style_button: QAction | None = None
        self.standard_style_button: QAction | None = None
        self.ram_usage_label: QLabel | None = None
        self.menu: QMenuBar | None = None

        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        self.translate_ui()
        self.set_objects_name()
        self.set_signals()
        self.init_list_model()
        self.set_bitrate_variants()
        self.set_settings_menu()
        self.calculate_saved_data_fill_and_check_debug()
        self.ui.start_button.setProperty("rebuild_status", self.data_fill_count)

    @logger.catch
    def translate_ui(self) -> None:
        """Перевод интерфейса"""
        self.setWindowTitle("MKVRebuilder")
        self.ui.source_button.setText(self.tr("Set source file"))
        self.ui.target_button.setText(self.tr("Set output directory"))
        self.ui.temp_button.setText(self.tr("Set temp directory"))
        self.ui.bitrate_label.setText(self.tr("Choose bitrate"))
        self.ui.start_button.setText(self.tr("Start rebuilding mkv"))
        self.ui.subtitles_button.setText(self.tr("Update subtitles"))
        self.ui.subtitles_button.setDisabled(True)
        self.ui.source_label.setText(self.tr("Empty"))
        self.ui.source_label.setProperty("source_empty", True)
        self.unpolish_and_polish_style(self.ui.source_label)
        if self.temp_path:
            self.ui.temp_label.setText(f"{self.temp_path}")
        else:
            self.ui.temp_label.setText(self.tr("Empty"))
            self.ui.temp_label.setProperty("temp_empty", True)
            self.unpolish_and_polish_style(self.ui.temp_label)
        if self.output_path:
            self.ui.target_label.setText(f"{self.output_path}")
        else:
            self.ui.target_label.setText(self.tr("Empty"))
            self.ui.target_label.setProperty("target_empty", True)
            self.ui.target_button.setProperty("disabled", True)
            self.ui.target_button.setDisabled(True)
            self.unpolish_and_polish_style(self.ui.target_label)

    @logger.catch
    def set_settings_menu(self) -> None:
        """Установить меню стилей"""
        self.black_style_button = QAction(self.tr("Black theme"), self)
        self.black_style_button.triggered.connect(self.set_black_style)

        self.standard_style_button = QAction(self.tr("Standard theme"), self)
        self.standard_style_button.triggered.connect(self.set_standard_style)

        self.menu = self.menuBar()
        style_menu = self.menu.addMenu(self.tr("Style"))

        style_menu.addAction(self.black_style_button)
        style_menu.addSeparator()
        style_menu.addAction(self.standard_style_button)
        style_menu.addSeparator()

    @logger.catch
    def set_objects_name(self) -> None:
        """Установка названий объектов для кнопок и тд"""
        self.ui.source_button.setObjectName("source_button")
        self.ui.target_button.setObjectName("target_button")
        self.ui.temp_button.setObjectName("temp_button")
        self.ui.bitrate_label.setObjectName("bitrate_label")
        self.ui.bitrate_box.setObjectName("bitrate_box")
        self.ui.start_button.setObjectName("start_button")
        self.ui.subtitles_button.setObjectName("subtitles_button")
        self.ui.source_label.setObjectName("source_label")
        self.ui.temp_label.setObjectName("temp_label")
        self.ui.target_label.setObjectName("target_label")
        self.ui.audio_list.setObjectName("audio_list")
        self.ui.subtitle_list.setObjectName("subtitle_list")
        self.setObjectName("main_layout")

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
        self.ui.source_button.clicked.connect(self.set_source_file)
        self.ui.target_button.clicked.connect(self.set_output_dir)
        self.ui.temp_button.clicked.connect(self.set_temp_dir)
        self.ui.subtitles_button.clicked.connect(self.fill_subtitle_list)
        self.ui.start_button.clicked.connect(self.open_rebuilder_widget)
        self.ui.audio_list.pressed.connect(self.set_track_id)
        self.ui.subtitle_list.pressed.connect(self.set_subtitle_id)
        self.ui.bitrate_box.currentTextChanged.connect(self.set_bitrate)

    @logger.catch
    def init_list_model(self) -> None:
        """Инициализация модели списка"""
        self.audio_model = QtGui.QStandardItemModel()
        self.ui.audio_list.setModel(self.audio_model)
        self.subtitle_model = QtGui.QStandardItemModel()
        self.ui.subtitle_list.setModel(self.subtitle_model)
        self.ui.audio_list.setSpacing(5)
        self.ui.subtitle_list.setSpacing(5)
        self.ui.audio_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.subtitle_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    @logger.catch
    def calculate_saved_data_fill_and_check_debug(self) -> None:
        """Подсчитать выполнение этапов для запуска конвертации и проверь включен ли дебаг"""
        if self.temp_path:
            self.data_fill_count += 1
            self.data_fill_count_dict.update(temp=1)
            if self.output_path:
                self.data_fill_count += 1
                self.ui.target_button.setProperty("disabled", False)
                self.unpolish_and_polish_style(self.ui.target_button)
                self.data_fill_count_dict.update(output=1)
        if settings.get_debug_status() is True:
            self.debug_thread.cpu_disc_usage_signal.connect(self.statusBar().showMessage)
            self.debug_thread.start()
        self.ui.start_button.setProperty("rebuild_status", self.data_fill_count)

    @logger.catch
    def calculate_data_fill(self) -> None:
        """Подсчет выполнения этапов для старта конвертации"""
        self.data_fill_count = 0
        for i in self.data_fill_count_dict:
            data = self.data_fill_count_dict.get(i)
            self.data_fill_count += data
            if self.data_fill_count == 4:
                self.ui.start_button.setText(self.tr("Start rebuilding mkv"))
        self.ui.start_button.setProperty("rebuild_status", self.data_fill_count)
        self.unpolish_and_polish_style(self.ui.start_button)
        logger.info(f"data_fill: {self.data_fill_count}")

    @logger.catch
    def set_black_style(self) -> None:
        """Установка темной темы"""
        with open("static/style/black_main.qss", "r") as file:
            style = file.read()
        self.setStyleSheet(style)
        settings.change_theme(True)

    @logger.catch
    def set_standard_style(self) -> None:
        """Установка стандартной темы"""
        self.setStyleSheet("")
        settings.change_theme(False)

    @logger.catch
    def unpolish_and_polish_style(self,  widget: Any) -> None:
        """Обновление стиля виджета с пользовательским свойсвоой"""
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    @logger.catch
    def set_bitrate(self, bitrate: str) -> None:
        """Установка битрейта"""
        self.bitrate = int(bitrate)

    @logger.catch
    def get_info_about_source_file_sound(self, source_path: str) -> list:
        """Сбор информации о звуковых дорожках в источнике"""
        mkv_merge_service.get_mkv_info(source_path)
        sound_tracks = mkv_merge_service.build_sound_info()
        return sound_tracks

    @logger.catch
    def get_info_about_source_file_subtitle(self) -> list:
        """Сбор информации о субтитрах в источнике"""
        subtitles = mkv_merge_service.build_subtitles_info()
        return subtitles

    @logger.catch
    def fill_audio_list(self, source_path: str) -> None:
        """Заполнение списка информацией о треках"""
        sound_tracks = self.get_info_about_source_file_sound(source_path)
        row_count = self.audio_model.rowCount()
        self.audio_model.removeRows(0, row_count)
        try:
            for audio_track in sound_tracks:
                track_id = audio_track.get("id")
                language = audio_track.get("language")
                codec = audio_track.get("format")
                try:
                    track_name = audio_track.get("name")
                    query = f"id: {track_id}\nformat: {codec}\nname: {track_name}\nlanguage: {language}"
                    item = QtGui.QStandardItem(query)
                    data = {"id": track_id, "codec": codec, "name": track_name, "lang": language}
                    item.setData(data)
                    self.audio_model.appendRow(item)
                except KeyError as key_exc:
                    query = f"id: {track_id}\n format: {codec}\n language: {language}"
                    item = QtGui.QStandardItem(query)
                    data = {"id": track_id, "codec": codec, "lang": language}
                    item.setData(data)
                    self.audio_model.appendRow(item)
        except Exception as exc:
            logger.error(f"{self.fill_audio_list.__name__} - {exc})")

    def fill_subtitle_list(self, status) -> None:
        """Заполнение списка информацией о субтитрах"""
        row_count = self.subtitle_model.rowCount()
        if status is True:
            subtitles = self.get_info_about_source_file_subtitle()
            self.subtitle_model.removeRows(0, row_count)
            try:
                for subtitle in subtitles:
                    sub_id = subtitle.get("id")
                    language = subtitle.get("language")
                    try:
                        sub_name = subtitle.get("name")
                        query = f"id: {sub_id}\nname: {sub_name}\nlanguage: {language}"
                        item = QtGui.QStandardItem(query)
                        data = {"id": sub_id, "name": sub_name, "lang": language}
                        item.setData(data)
                        self.subtitle_model.appendRow(item)
                    except KeyError as key_exc:
                        query = f"id: {sub_id}\n language: {language}"
                        item = QtGui.QStandardItem(query)
                        data = {"id": sub_id, "lang": language}
                        item.setData(data)
                        self.subtitle_model.appendRow(item)
            except Exception as exc:
                logger.error(f"{self.fill_subtitle_list.__name__} - {exc})")
        else:
            self.subtitle_model.removeRows(0, row_count)
            if self.subtitle_data:
                self.subtitle_data = None

    @logger.catch
    def off_subtitle_list(self) -> None:
        """Отчистить и отключить список субтитров"""
        row_count = self.subtitle_model.rowCount()
        self.subtitle_model.removeRows(0, row_count)
        self.ui.subtitles_button.setChecked(False)
        self.subtitle_data = None

    @logger.catch
    def set_source_file(self) -> None:
        """Выбор источника"""
        source_path = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Select source"),  filter="mkv(*.mkv)")[0]
        if source_path:
            mkv_name = source_path.replace(".mkv", "")
            mkv_name = mkv_name.split("/")
            data_len = len(mkv_name)
            new_mkv_name = mkv_name[data_len - 1]
            new_mkv_name = f"{new_mkv_name}.rebuilded.mkv"
            self.source_file_name = new_mkv_name
            self.source_path = source_path
            self.ui.source_label.setText(f"{source_path}")
            self.fill_audio_list(source_path)
            self.ui.subtitles_button.setDisabled(False)
            self.ui.target_button.setDisabled(False)
            self.ui.target_button.setProperty("disabled", False)
            self.off_subtitle_list()
            self.ui.source_label.setProperty("source_empty", False)
            self.unpolish_and_polish_style(self.ui.source_label)
            self.unpolish_and_polish_style(self.ui.target_button)
            self.data_fill_count_dict.update(source=1)
            self.calculate_data_fill()
            if self.output_path:
                self.output_file = f"{self.output_path}/{self.source_file_name}"
                self.ui.target_label.setText(f"{self.output_path}/{self.source_file_name}")
                self.ui.target_label.setProperty("source_empty", False)
                self.unpolish_and_polish_style(self.ui.target_label)
        else:
            pass

    @logger.catch
    def set_output_dir(self) -> None:
        """Целевая директория для сохранения"""
        output_path = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Select target"))
        if output_path:
            self.output_path = output_path
            ini_settings.change_output_dir_section(output_path)
            self.ui.target_label.setProperty("target_empty", False)
            self.unpolish_and_polish_style(self.ui.target_label)
            self.data_fill_count_dict.update(output=1)
            self.calculate_data_fill()
            if self.source_file_name:
                self.output_file = f"{output_path}/{self.source_file_name}"
                self.ui.target_label.setText(f"{output_path}/{self.source_file_name}")
            else:
                self.ui.target_label.setText(f"{output_path}/")
        else:
            pass

    @logger.catch
    def set_temp_dir(self) -> None:
        """Выбор папки временных файлов"""
        temp_dir = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Select temp dir"))
        if temp_dir:
            self.data_fill_count_dict.update(temp=1)
            self.calculate_data_fill()
            self.ui.temp_label.setText(f"{temp_dir}")
            ini_settings.change_temp_dir_section(temp_dir)
            self.temp_path = temp_dir
            self.ui.temp_label.setProperty("temp_empty", False)
            self.unpolish_and_polish_style(self.ui.temp_label)
        else:
            pass

    @logger.catch
    def set_track_id(self, index) -> None:
        """Установка id звуковой дорожки"""
        track = self.ui.audio_list.model().itemFromIndex(index)
        self.track_data = track.data()
        codec = self.track_data.get("codec")
        self.data_fill_count_dict.update(sound=1)
        self.calculate_data_fill()
        if codec in self.restricted_codec_list:
            self.restricted_codec = codec
            self.ui.bitrate_box.setDisabled(True)
        else:
            self.ui.bitrate_box.setDisabled(False)
            self.restricted_codec = None

    @logger.catch
    def set_subtitle_id(self, index) -> None:
        """Установка id субтитров"""
        subtitle_data = self.ui.subtitle_list.model().itemFromIndex(index)
        self.subtitle_data = subtitle_data.data()

    @logger.catch
    def open_rebuilder_widget(self) -> None:
        """Открытие виджета сборки"""
        temp_dir = self.ui.temp_label.text()
        target_file = self.ui.target_label.text()
        source_file = self.ui.source_label.text()
        if source_file == "Empty" or source_file == "Не выбрано":
            self.ui.start_button.setText(self.tr("Source file: dont selected"))
        elif target_file == "Empty" or target_file == "Не выбрано":
            self.ui.start_button.setText(self.tr("Output dir: dont selected"))
        elif temp_dir == "Empty" or temp_dir == "Не выбрано":
            self.ui.start_button.setText(self.tr("Temp dir: dont selected"))
        elif not self.track_data:
            self.ui.start_button.setText(self.tr("Sound track: dont selected"))
        else:
            self.rebuilder_widget = RebuilderWidget(self, self.source_path, self.output_file, self.track_data,
                                                    self.subtitle_data, self.temp_path, self.bitrate,
                                                    self.restricted_codec)
            self.rebuilder_widget.show()

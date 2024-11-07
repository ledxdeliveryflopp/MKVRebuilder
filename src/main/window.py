from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QBrush, QRadialGradient, QColor
from PySide6.QtWidgets import QAbstractItemView
from loguru import logger

from src.info.service import mkv_merge_service
from src.main.widget_ui import UiMainWindow
from src.rebuilder.widget import SettingsWidget

from src.settings.config import ini_settings


class MainWindow(QtWidgets.QMainWindow):
    """Класс основного окна/виджета"""

    def __init__(self) -> None:
        super().__init__()
        self.source_file_name: str = None
        self.source_file_path: str = None
        self.output_file: str = None
        self.temp_path: str = ini_settings.get_temp_dir()
        self.output_path: str = ini_settings.get_output_dir()
        self.track_data: dict = None
        self.subtitle_data: dict | None = None
        self.bitrate: int = 192
        self.audio_model = None
        self.subtitle_model = None
        self.settings_widget: QtWidgets = None
        self.ui = UiMainWindow()
        self.ui.setupUi(self)
        self.translate_ui()
        self.set_signals()
        self.init_list_model()
        self.set_bitrate_variants()

    @logger.catch
    def translate_ui(self) -> None:
        """Перевод интерфейса"""
        self.ui.source_button.setText(self.tr("Set source file"))
        self.ui.target_button.setDisabled(True)
        self.ui.target_button.setText(self.tr("Set output directory"))
        self.ui.temp_button.setText(self.tr("Set temp directory"))
        self.ui.bitrate_label.setText(self.tr("Choose bitrate"))
        self.ui.settings_button.setText(self.tr("Configurate ac3 file"))
        self.ui.subtitles_button.setText(self.tr("Update subtitles"))
        self.ui.subtitles_button.setDisabled(True)
        self.ui.source_label.setText(self.tr("Empty"))
        if self.temp_path:
            self.ui.temp_label.setText(f"{self.temp_path}")
        else:
            self.ui.temp_label.setText(self.tr("Empty"))
        if self.output_path:
            self.ui.target_label.setText(f"{self.output_path}")
        else:
            self.ui.target_label.setText(self.tr("Empty"))

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
        self.ui.settings_button.clicked.connect(self.open_settings_widget)
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
        self.ui.audio_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.subtitle_list.setEditTriggers(QAbstractItemView.NoEditTriggers)

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

    @logger.catch
    def off_subtitle_list(self) -> None:
        """Отчистить и отключить список субтитров"""
        row_count = self.subtitle_model.rowCount()
        self.subtitle_model.removeRows(0, row_count)
        self.ui.subtitles_button.setChecked(False)

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
            self.source_file_path = source_path
            self.ui.source_label.setText(f"{source_path}")
            self.fill_audio_list(source_path)
            self.ui.subtitles_button.setDisabled(False)
            self.ui.target_button.setDisabled(False)
            self.off_subtitle_list()
            if self.output_path:
                self.output_file = f"{self.output_path}/{self.source_file_name}"
                self.ui.target_label.setText(f"{self.output_path}/{self.source_file_name}")
        else:
            pass

    @logger.catch
    def set_output_dir(self) -> None:
        """Целевая директория для сохранения"""
        output_path = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Select target"))
        if output_path:
            self.output_path = output_path
            ini_settings.change_output_dir_section(output_path, self.temp_path)
            if self.source_file_name:
                self.output_file = f"{output_path}/{self.source_file_name}"
                self.ui.target_label.setText(f"{output_path}/{self.source_file_name}")
        else:
            pass

    @logger.catch
    def set_temp_dir(self) -> None:
        """Выбор папки временных файлов"""
        temp_dir = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Select temp dir"))
        if temp_dir:
            self.ui.temp_label.setText(f"{temp_dir}")
            ini_settings.change_temp_dir_section(temp_dir, self.output_path)
            self.temp_path = temp_dir
        else:
            pass

    @logger.catch
    def set_selected_brush(self, model: QtGui.QStandardItem) -> None:
        """Установка цвета при выборе объекта в списке звука/субтитров"""
        gradient = QRadialGradient(50, 50, 50, 50, 50)
        gradient.setColorAt(0, QColor.fromRgbF(0, 1, 0, 1))
        gradient.setColorAt(1, QColor.fromRgbF(0, 0, 0, 0))
        brush = QBrush(gradient)
        self.cansel_selected_brush(model)
        model.setBackground(brush)

    @logger.catch
    def cansel_selected_brush(self, model: QtGui.QStandardItem) -> None:
        """Установка цвета при отмене выборе объекта в списке звука/субтитров"""
        gradient = QRadialGradient(50, 50, 50, 50, 50)
        gradient.setColorAt(0, QColor.fromRgbF(255, 255, 255, 0.9))
        brush = QBrush(gradient)
        model.setBackground(brush)

    @logger.catch
    def set_track_id(self, index) -> None:
        """Установка id звуковой дорожки"""
        track = self.ui.audio_list.model().itemFromIndex(index)
        self.track_data = track.data()

    @logger.catch
    def set_subtitle_id(self, index) -> None:
        """Установка id субтитров"""
        subtitle_data = self.ui.subtitle_list.model().itemFromIndex(index)
        self.subtitle_data = subtitle_data.data()

    @logger.catch
    def open_settings_widget(self) -> None:
        temp_dir = self.ui.temp_label.text()
        target_file = self.ui.target_label.text()
        source_file = self.ui.source_label.text()
        if temp_dir == "Empty" or target_file == "Empty" or source_file == "Empty" or not self.track_data:
            pass
        else:
            self.settings_widget = SettingsWidget(main_window=self, source_file=self.source_file_path,
                                                  output_file=self.output_file, track_data=self.track_data,
                                                  subtitle_data=self.subtitle_data, temp_path=self.temp_path)
            self.settings_widget.show()

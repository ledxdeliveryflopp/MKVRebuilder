import os
import subprocess
from time import time

from PySide6 import QtWidgets, QtCore
from loguru import logger

from src.rebuilder.utils import generate_temp_dir, clear_temp_dts, clear_temp_ac3, clear_temp_srt, clear_temp_eac3
from src.rebuilder.widget_ui import UiRebuilderWidget
from src.settings.settings import settings
from src.settings.thread_manager import ThreadManager
from static.eac3.utils import get_eac3_path
from static.mkv_tools.utils import get_mkv_tools_path


class RebuilderWidget(QtWidgets.QWidget, ThreadManager):
    """Виджет извлечения/конвертации/сборки"""

    def __init__(self, main_window: QtWidgets.QMainWindow,
                 source_path: str, output_file: str, track_data: dict, subtitle_data: dict | None, temp_path: str,
                 bitrate: int, restricted_codec: str):
        super().__init__()
        self.main_window = main_window
        self.source_path: str = source_path
        self.output_file: str = output_file
        self.track_data: dict = track_data
        self.subtitle_data: dict | None = subtitle_data
        self.temp_path: str = temp_path
        self.restricted_codec: str = restricted_codec
        self.bitrate: int = bitrate

        self.track_id: int | None = None
        self.track_name: int | None = None
        self.track_lang: int | None = None

        self.subtitle_id: int | None = None
        self.subtitle_name: int | None = None
        self.subtitle_lang: int | None = None

        self.temp_dir: dict | None = None
        self.subtitle_temp_path_id: str | None = None
        self.sound_temp_path_id: str | None = None

        self.extract_eac3_track_path: str | None = None
        self.extract_ac3_track_path: str | None = None
        self.extract_dts_track_path: str | None = None
        self.extract_srt_path: str | None = None

        self.sound_temp_dir: str | None = None
        self.subtitle_temp_dir: str | None = None

        self.dts_path: str | None = None
        self.ac3_path: str | None = None
        self.eac3_path: str | None = None
        self.subtitle_path: str | None = None

        self.mkv_merge_path: str | None = None
        self.mkv_extract_path: str | None = None
        self.ac3_converter: str | None = None

        self.ui = UiRebuilderWidget()
        self.ui.setupUi(self)
        self.translate_ui()
        self.set_theme()
        self.set_mkv_ac3_tools_path()

    @logger.catch
    def translate_ui(self) -> None:
        """Перевод интерфейса"""
        self.setWindowTitle("MKVRebuilder: rebuilding")
        self.ui.mkv.setText(self.tr("build new mkv: Not started"))
        self.setWindowFlags(QtCore.Qt.WindowType.WindowMinimizeButtonHint)
        if self.restricted_codec:
            self.ui.ac3.setText(self.tr("extract subtitle: Skip"))
            self.ui.ac3.setProperty("skip", True)
        else:
            self.ui.ac3.setText(self.tr("convert dts to ac3: Not started"))
        if self.subtitle_data:
            self.ui.subtitle.setText(self.tr("extract subtitle: Not started"))
        else:
            self.ui.subtitle.setText(self.tr("extract subtitle: Skip"))
            self.ui.subtitle.setProperty("skip", True)

    @logger.catch
    def set_mkv_ac3_tools_path(self) -> None:
        """Определение местоположение mkvtools, eac3"""
        mkv_tools_path = get_mkv_tools_path()
        eac3_path = get_eac3_path()
        self.mkv_extract_path = fr"{mkv_tools_path}\mkvextract.exe"
        self.mkv_merge_path = fr"{mkv_tools_path}\mkvmerge.exe"
        self.ac3_converter = fr"{eac3_path}\eac3to.exe"

    @logger.catch
    def set_black_style(self) -> None:
        """Установка темной темы"""
        with open("static/style/black_rebuilder.qss", "r") as file:
            style = file.read()
        self.setStyleSheet(style)

    @logger.catch
    def set_standard_style(self) -> None:
        """Установка стандартной темы"""
        self.setStyleSheet("")

    @logger.catch
    def set_theme(self):
        status = settings.get_theme_status()
        if status is True:
            self.set_black_style()
        else:
            self.set_standard_style()

    def showEvent(self, event):
        self.main_window.setEnabled(False)
        self.start_work()

    @logger.catch
    def set_data(self) -> None:
        """Установка необходимой информации о звуковой дорожке и субтитрах"""
        self.track_id = self.track_data.get("id")
        self.track_lang = self.track_data.get("lang")
        try:
            self.track_name = self.track_data.get("name")
        except KeyError as track_name_none:
            self.track_name = "empty"
        if self.subtitle_data:
            try:
                self.subtitle_id = self.subtitle_data.get("id")
                self.subtitle_lang = self.subtitle_data.get("lang")
            except KeyError as subtitle_name_none:
                self.subtitle_name = "empty"

    @logger.catch
    def set_temp_dir(self) -> None:
        """Установка директории для сохранения звуковых дорожек и субтитров"""
        if self.subtitle_data:
            self.temp_dir = generate_temp_dir(self.temp_path, self.track_id, self.subtitle_id)
            self.subtitle_temp_path_id = self.temp_dir.get("sub_id")
            self.sound_temp_path_id = self.temp_dir.get("sound_id")
            self.sound_temp_dir = self.temp_dir.get("sound")
            self.subtitle_temp_dir = self.temp_dir.get("sub")
        else:
            self.temp_dir = generate_temp_dir(self.temp_path, self.track_id, None)
            self.sound_temp_path_id = self.temp_dir.get("sound_id")
            self.sound_temp_dir = self.temp_dir.get("sound")

    @logger.catch
    def set_subtitle_path(self):
        if self.subtitle_data:
            subtitles_path = f"{self.subtitle_temp_dir}{self.subtitle_id}.srt"
            self.subtitle_path = os.path.abspath(subtitles_path)
            self.extract_srt_path = f"{self.subtitle_temp_path_id}{self.subtitle_id}.srt"

    @logger.catch
    def set_sound_track_path(self) -> None:
        """Установка файлов для сохранения звуковой дорожки"""
        ac3_path = f"{self.sound_temp_dir}{self.track_id}.ac3"
        self.ac3_path = os.path.abspath(ac3_path)
        if self.restricted_codec == "AC-3":
            self.extract_ac3_track_path = f"{self.sound_temp_path_id}{self.track_id}.ac3"
        elif self.restricted_codec == "E-AC-3":
            eac3_path = f"{self.sound_temp_dir}{self.track_id}.eac3"
            self.eac3_path = os.path.abspath(eac3_path)
            self.extract_eac3_track_path = f"{self.sound_temp_path_id}{self.track_id}.eac3"
        else:
            dts_path = f"{self.sound_temp_dir}{self.track_id}.dts"
            self.dts_path = os.path.abspath(dts_path)
            self.extract_dts_track_path = f"{self.sound_temp_path_id}{self.track_id}.dts"

    @logger.catch
    def start_work(self) -> None:
        """Начало работы"""
        logger.info(f"restricted_codec = {self.restricted_codec}")
        logger.info(f"sub data = {self.subtitle_data}")
        logger.info(f"track data = {self.track_data}")
        logger.info(f"bitrate = {self.bitrate}")
        self.set_data()
        self.set_temp_dir()
        self.set_sound_track_path()
        self.set_subtitle_path()
        if self.restricted_codec == "AC-3":
            self.thread_manager.start(self.extract_ac3_track)
        elif self.restricted_codec == "E-AC-3":
            self.thread_manager.start(self.extract_eac3_track)
        else:
            self.thread_manager.start(self.extract_dts_track)

    @logger.catch
    def extract_ac3_track(self):
        """Извлечь звуковую дорожку ac3"""
        t1 = time()
        command = subprocess.Popen([f"{self.mkv_extract_path}", "tracks", self.source_path, self.extract_ac3_track_path],
                                   stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        logger.info(f"{self.extract_ac3_track.__name__}: {command.stdout.readline()}")
        for line in command.stdout:
            self.ui.sound.setText(self.tr(f"extract sound: {line}"))
        t2 = time()
        summary_time = t2 - t1
        elapsed = summary_time / 60
        self.ui.sound.setText(self.tr(f'extract sound, progress 100: %.3f minutes' % elapsed))
        if self.subtitle_data:
            self.thread_manager.start(self.extract_sub)
        else:
            self.thread_manager.start(self.build_new_mkv)

    @logger.catch
    def extract_dts_track(self):
        """Извлечь звуковую дорожку dts"""
        t1 = time()
        command = subprocess.Popen([f"{self.mkv_extract_path}", "tracks", self.source_path, self.extract_dts_track_path],
                                   stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        logger.info(f"{self.extract_dts_track.__name__}: {command.stdout.readline()}")
        for line in command.stdout:
            self.ui.sound.setText(self.tr(f"extract sound: {line}"))
        t2 = time()
        summary_time = t2 - t1
        elapsed = summary_time / 60
        self.ui.sound.setText(self.tr(f'extracting sound, progress 100: %.3f minutes' % elapsed))
        if self.subtitle_data:
            self.thread_manager.start(self.extract_sub)
        else:
            self.thread_manager.start(self.convert_to_ac3)

    @logger.catch
    def extract_eac3_track(self):
        """Извлечь звуковую дорожку E-AC-3"""
        t1 = time()
        command = subprocess.Popen([f"{self.mkv_extract_path}", "tracks", self.source_path, self.extract_eac3_track_path],
                                   stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        logger.info(f"{self.extract_eac3_track.__name__}: {command.stdout.readline()}")
        for line in command.stdout:
            self.ui.sound.setText(self.tr(f"extract sound: {line}"))
        t2 = time()
        summary_time = t2 - t1
        elapsed = summary_time / 60
        self.ui.sound.setText(self.tr(f'extracting sound, progress 100: %.3f minutes' % elapsed))
        if self.subtitle_data:
            self.thread_manager.start(self.extract_sub)
        else:
            self.thread_manager.start(self.build_new_mkv_with_eac3_codec)

    @logger.catch
    def extract_sub(self):
        """Извлечь субтитры"""
        t1 = time()
        command = subprocess.Popen([f"{self.mkv_extract_path}", "tracks", self.source_path, self.extract_srt_path],
                                   stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        logger.info(f"{self.extract_sub.__name__}: {command.stdout.readline()}")
        for line in command.stdout:
            self.ui.subtitle.setText(self.tr(f"extract subtitle: {line}"))
        t2 = time()
        summary_time = t2 - t1
        elapsed = summary_time / 60
        self.ui.subtitle.setText(self.tr(f'extracting subtitles, progress 100: %.3f minutes' % elapsed))
        if self.restricted_codec == "E-AC-3":
            self.thread_manager.start(self.build_new_mkv_with_eac3_codec)
        elif self.restricted_codec == "AC-3":
            self.thread_manager.start(self.build_new_mkv)
        else:
            self.thread_manager.start(self.convert_to_ac3)

    @logger.catch
    def convert_to_ac3(self):
        """Конвертировать dts в ac3"""
        t1 = time()
        logger.info(f"ac3 path - {self.ac3_path}")
        self.ui.ac3.setText(self.tr("converting dts to ac3"))
        subprocess.run([f"{self.ac3_converter}", self.dts_path, self.ac3_path, f"-{self.bitrate}", f"-down6"],
                       stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        t2 = time()
        summary_time = t2 - t1
        elapsed = summary_time / 60
        self.ui.ac3.setText(self.tr(f'dts to ac3, progress 100: %.3f minutes' % elapsed))
        self.thread_manager.start(self.build_new_mkv)

    @logger.catch
    def build_new_mkv_with_eac3_codec(self):
        """Собрать новый mkv с eac3"""
        t1 = time()
        sound_metadata = f'--language 0:{self.track_lang} --track-name 0:"{self.track_name}"'
        logger.info("start rebuild with E-AC-3")
        if self.subtitle_data:
            sub_command = f'--language 0:{self.subtitle_lang} --track-name 0:"{self.subtitle_name}"'
            command = subprocess.Popen(f'{self.mkv_merge_path} -o {self.output_file} -A -S {self.source_path} {sound_metadata} {self.eac3_path} {sub_command} {self.subtitle_path}',
                                       stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for line in command.stdout:
                self.ui.mkv.setText(self.tr(f"rebuild mkv: {line}"))
            t2 = time()
            summary_time = t2 - t1
            elapsed = summary_time / 60
            self.ui.mkv.setText(self.tr(f'rebuild mkv, progress 100: %.3f minutes' % elapsed))
            self.main_window.setEnabled(True)
            clear_temp_eac3(self.eac3_path)
            clear_temp_srt(self.subtitle_path)
        else:
            command = subprocess.Popen(f'{self.mkv_merge_path} -o {self.output_file} -A -S {self.source_path} {sound_metadata} {self.eac3_path}',
                                       stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for line in command.stdout:
                self.ui.mkv.setText(self.tr(f"rebuild mkv: {line}"))
            t2 = time()
            summary_time = t2 - t1
            elapsed = summary_time / 60
            self.ui.mkv.setText(self.tr(f'rebuild mkv, progress 100: %.3f minutes' % elapsed))
            self.main_window.setEnabled(True)
            clear_temp_eac3(self.eac3_path)

    @logger.catch
    def build_new_mkv(self):
        """Собрать новый mkv"""
        t1 = time()
        sound_metadata = f'--language 0:{self.track_lang} --track-name 0:"{self.track_name}"'
        logger.info("start rebuild with AC-3")
        if self.subtitle_data:
            sub_command = f'--language 0:{self.subtitle_lang} --track-name 0:"{self.subtitle_name}"'
            command = subprocess.Popen(f'{self.mkv_merge_path} -o {self.output_file} -A -S {self.source_path} {sound_metadata} {self.ac3_path} {sub_command} {self.subtitle_path}',
                                       stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for line in command.stdout:
                self.ui.mkv.setText(self.tr(f"rebuild mkv: {line}"))
            t2 = time()
            summary_time = t2 - t1
            elapsed = summary_time / 60
            self.ui.mkv.setText(self.tr(f'rebuild mkv, progress 100: %.3f minutes' % elapsed))
            self.main_window.setEnabled(True)
            clear_temp_dts(self.dts_path)
            clear_temp_ac3(self.ac3_path)
            clear_temp_srt(self.subtitle_path)
        else:
            command = subprocess.Popen(f'{self.mkv_merge_path} -o {self.output_file} -A -S {self.source_path} {sound_metadata} {self.ac3_path}',
                                       stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for line in command.stdout:
                self.ui.mkv.setText(self.tr(f"rebuild mkv: {line}"))
            t2 = time()
            summary_time = t2 - t1
            elapsed = summary_time / 60
            self.ui.mkv.setText(self.tr(f'rebuild mkv, progress 100: %.3f minutes' % elapsed))
            self.main_window.setEnabled(True)
            clear_temp_dts(self.dts_path)
            clear_temp_ac3(self.ac3_path)

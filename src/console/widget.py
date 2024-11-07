import os
import subprocess
from functools import partial
from time import time

from PySide6 import QtWidgets, QtCore
from loguru import logger

from src.console.utils import generate_temp_dir
from src.console.widget_ui import Ui_console_widget
from src.settings.thread_manager import ThreadManager
from static.eac3.utils import get_eac3_path
from static.mkv_tools.utils import get_mkv_tools_path


class ConsoleWidget(QtWidgets.QWidget, ThreadManager):
    """Виджет извлечения/конвертации/сборки"""

    def __init__(self, main_window: QtWidgets.QMainWindow,
                 source_file: str, output_file: str, track_data: dict, subtitle_data: dict | None, temp_path: str,
                 bitrate: int, eac3_mode: bool):
        super().__init__()
        self.main_window = main_window
        self.source_file: str = source_file
        self.output_file: str = output_file
        self.track_data: dict = track_data
        self.subtitle_data: dict | None = subtitle_data
        self.track_id: int = None
        self.track_name: int = None
        self.track_lang: int = None
        self.subtitle_id: int | None = 11
        self.subtitle_name: int | None = None
        self.subtitle_lang: int | None = None
        self.temp_path: str = temp_path
        self.bitrate: int = bitrate
        self.ac3_path: str = None
        self.eac3_path: str = None
        self.sub_path: str = None
        self.mkv_merge_path: str = None
        self.mkv_extract_path: str = None
        self.ac3_converter: str = None
        self.eac3_mode: bool = eac3_mode
        self.model = None
        self.ui = Ui_console_widget()
        self.ui.setupUi(self)
        self.translate_ui()
        self.set_mkv_ac3_tools_path()

    @logger.catch
    def translate_ui(self) -> None:
        """Перевод интерфейса"""
        self.ui.subtitle.setText(self.tr("extract subtitle: Not started"))
        self.ui.ac3.setText(self.tr("convert dts to ac3: Not started"))
        self.ui.mkv.setText(self.tr("build new mkv: Not started"))
        self.setWindowFlags(QtCore.Qt.WindowType.WindowMinimizeButtonHint)

    @logger.catch
    def set_mkv_ac3_tools_path(self) -> None:
        """Определение местоположение mkvtools, eac3"""
        mkv_tools_path = get_mkv_tools_path()
        eac3_path = get_eac3_path()
        self.mkv_extract_path = fr"{mkv_tools_path}\mkvextract.exe"
        self.mkv_merge_path = fr"{mkv_tools_path}\mkvmerge.exe"
        self.ac3_converter = fr"{eac3_path}\eac3to.exe"

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
            self.track_name = "Auto fill name"
        if self.subtitle_data:
            self.subtitle_id = self.subtitle_data.get("id")
            self.subtitle_name = self.subtitle_data.get("name")
            self.subtitle_lang = self.subtitle_data.get("lang")

    @logger.catch
    def start_work(self) -> None:
        """Начало работы"""
        self.set_data()
        if self.subtitle_data:
            temp_path = generate_temp_dir(self.temp_path, self.track_id, self.subtitle_id)
            subtitle_temp_path_id = temp_path.get("sub_id")
            self.thread_manager.start(partial(self.extract_track, temp_path, subtitle_temp_path_id))
        else:
            temp_path = generate_temp_dir(self.temp_path, self.track_id, None)
            self.thread_manager.start(partial(self.extract_track, temp_path, None))

    @logger.catch
    def extract_track(self, temp_path: dict, subtitle_temp_path_id: str | None):
        """Извлечь звуковую дорожку"""
        t1 = time()
        sound_temp_path = temp_path.get("sound_id")
        if self.eac3_mode is True:
            sound_track_path = f"{sound_temp_path}{self.track_id}.eac3"
        elif not self.bitrate:
            sound_track_path = f"{sound_temp_path}{self.track_id}.ac3"
        else:
            sound_track_path = f"{sound_temp_path}{self.track_id}.dts"
        command = subprocess.Popen([f"{self.mkv_extract_path}", "tracks", self.source_file, sound_track_path],
                                   stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        logger.info(f"{self.extract_track.__name__}: {command.stdout.readline()}")
        for line in command.stdout:
            self.thread_manager.start(self.ui.sound.setText(self.tr(f"extract sound: {line}")))
        t2 = time()
        summary_time = t2 - t1
        elapsed = summary_time / 60
        self.ui.sound.setText(self.tr(f'extracting sound track progress 100: %.3f minutes' % elapsed))
        if subtitle_temp_path_id:
            self.thread_manager.start(partial(self.extract_sub, subtitle_temp_path_id, temp_path))
        elif self.eac3_mode is True:
            sound_path = temp_path.get("sound")
            eac3_path = f"{sound_path}{self.track_id}.eac3"
            eac3_path_fixed = os.path.abspath(eac3_path)
            self.eac3_path = eac3_path_fixed
            self.ui.subtitle.setText(self.tr("Skipped"))
            self.ui.ac3.setText(self.tr("Skipped"))
            self.thread_manager.start(partial(self.build_new_mkv))
        elif not self.bitrate:
            sound_path = temp_path.get("sound")
            ac3_path = f"{sound_path}{self.track_id}.ac3"
            ac3_path_fixed = os.path.abspath(ac3_path)
            self.ac3_path = ac3_path_fixed
            self.ui.subtitle.setText(self.tr("Skipped"))
            self.ui.ac3.setText(self.tr("Skipped"))
            self.thread_manager.start(partial(self.build_new_mkv))
        else:
            self.thread_manager.start(partial(self.convert_to_ac, temp_path))

    @logger.catch
    def extract_sub(self, subtitle_temp_path_id: str, temp_path: dict):
        """Извлечь субтитры"""
        t1 = time()
        srt_path = f"{subtitle_temp_path_id}{self.subtitle_id}.srt"
        subtitles_path_dict = temp_path.get("sub")
        subtitles_path = f"{subtitles_path_dict}{self.subtitle_id}.srt"
        srt_path_fixed = os.path.abspath(subtitles_path)
        self.sub_path = srt_path_fixed
        command = subprocess.Popen([f"{self.mkv_extract_path}", "tracks", self.source_file, srt_path],
                                   stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        logger.info(f"{self.extract_sub.__name__}: {command.stdout.readline()}")
        for line in command.stdout:
            self.thread_manager.start(self.ui.subtitle.setText(self.tr(f"extract subtitle: {line}")))
        t2 = time()
        summary_time = t2 - t1
        elapsed = summary_time / 60
        self.ui.subtitle.setText(self.tr(f'extracting subtitles progress 100: %.3f minutes' % elapsed))
        if self.eac3_mode is True:
            sound_path = temp_path.get("sound")
            eac3_path = f"{sound_path}{self.track_id}.eac3"
            eac3_path_fixed = os.path.abspath(eac3_path)
            self.eac3_path = eac3_path_fixed
            self.ui.ac3.setText(self.tr("Skipped"))
            self.thread_manager.start(partial(self.build_new_mkv))
        elif not self.bitrate:
            sound_path = temp_path.get("sound")
            ac3_path = f"{sound_path}{self.track_id}.ac3"
            ac3_path_fixed = os.path.abspath(ac3_path)
            self.ac3_path = ac3_path_fixed
            self.ui.ac3.setText(self.tr("Skipped"))
            self.thread_manager.start(partial(self.build_new_mkv))
        elif temp_path and self.bitrate:
            self.thread_manager.start(partial(self.convert_to_ac, temp_path))

    @logger.catch
    def convert_to_ac(self, temp_path: dict):
        """Конвертировать dts в ac3"""
        logger.info(f"temp_path - {self.temp_path}")
        t1 = time()
        sound_path = temp_path.get("sound")
        dts_path = f"{sound_path}{self.track_id}.dts"
        ac3_path = f"{sound_path}{self.track_id}.ac3"
        ac3_path_fixed = os.path.abspath(ac3_path)
        self.ac3_path = ac3_path_fixed
        logger.info(f"ac3 path - {self.ac3_path}")
        self.ui.ac3.setText(self.tr("converting dts to ac3"))
        subprocess.run([f"{self.ac3_converter}", dts_path, self.ac3_path, f"-{self.bitrate}", f"-down6"],
                       stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        t2 = time()
        summary_time = t2 - t1
        elapsed = summary_time / 60
        self.ui.ac3.setText(self.tr(f'dts to ac3 progress 100: %.3f minutes' % elapsed))
        self.thread_manager.start(self.build_new_mkv)

    @logger.catch
    def build_new_mkv(self):
        """Собрать новый mkv"""
        t1 = time()
        lang_name_command = f'--language 0:{self.track_lang} --track-name 0:"{self.track_name}"'
        if self.subtitle_data and self.eac3_mode is True:
            sub_command = f'--language 0:{self.subtitle_lang} --track-name 0:"{self.subtitle_name}"'
            command = subprocess.Popen(
                f'{self.mkv_merge_path} -o {self.output_file} -A -S {self.source_file} {lang_name_command} {self.eac3_path} {sub_command} {self.sub_path}',
                stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for line in command.stdout:
                self.ui.mkv.setText(self.tr(f"rebuild mkv: {line}"))
            t2 = time()
            summary_time = t2 - t1
            elapsed = summary_time / 60
            self.ui.mkv.setText(self.tr(f'rebuild mkv progress 100: %.3f minutes' % elapsed))
            self.main_window.setEnabled(True)
        elif not self.subtitle_data and self.eac3_mode is True:
            command = subprocess.Popen(rf'{self.mkv_merge_path} -o {self.output_file} -A {self.source_file} {lang_name_command} {self.eac3_path}',
                                        stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for line in command.stdout:
                self.ui.mkv.setText(self.tr(f"rebuild mkv without subs: {line}"))
            t2 = time()
            summary_time = t2 - t1
            elapsed = summary_time / 60
            self.ui.mkv.setText(self.tr(f'rebuild mkv progress 100: %.3f minutes' % elapsed))
            self.main_window.setEnabled(True)
        if self.subtitle_data:
            sub_command = f'--language 0:{self.subtitle_lang} --track-name 0:"{self.subtitle_name}"'
            command = subprocess.Popen(f'{self.mkv_merge_path} -o {self.output_file} -A -S {self.source_file} {lang_name_command} {self.ac3_path} {sub_command} {self.sub_path}',
                                       stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            logger.info(f"{self.build_new_mkv.__name__} with subs: {command.stdout.readline()}")
            for line in command.stdout:
                self.ui.mkv.setText(self.tr(f"rebuild mkv: {line}"))
            t2 = time()
            summary_time = t2 - t1
            elapsed = summary_time / 60
            self.ui.mkv.setText(self.tr(f'rebuild mkv progress 100: %.3f minutes' % elapsed))
            self.main_window.setEnabled(True)
            # self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)
        elif not self.subtitle_data:
            command = subprocess.Popen(rf'{self.mkv_merge_path} -o {self.output_file} -A {self.source_file} {lang_name_command} {self.ac3_path}',
                                       stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            logger.info(f"{self.build_new_mkv.__name__} no subs: {command.stdout.readline()}")
            for line in command.stdout:
                self.ui.mkv.setText(self.tr(f"rebuild mkv without subs: {line}"))
            t2 = time()
            summary_time = t2 - t1
            elapsed = summary_time / 60
            self.ui.mkv.setText(self.tr(f'rebuild mkv progress 100: %.3f minutes' % elapsed))
            self.main_window.setEnabled(True)
            # self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint)

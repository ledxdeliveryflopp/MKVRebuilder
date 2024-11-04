import json
import os
import string
import subprocess
from dataclasses import dataclass
import random
from loguru import logger

from src.info.utils import generate_temp_dir


@dataclass
class InfoService:
    """Сервис взаимодействия с MKV"""

    @staticmethod
    @logger.catch
    def get_mkv_info(mkv_path: str) -> None:
        """Сбор информации о mkv"""
        logger.info("collecting info about mkv")
        mkv_merge_path = r"I:\Python_Projects\MKVAudioCut\mkv_tools\mkvmerge.exe"
        subprocess.run([mkv_merge_path, "-r", "track_info.json", "-J", mkv_path], stdout=subprocess.PIPE,
                       text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        logger.info("info collected")

    @logger.catch
    def get_tracks_audio(self) -> None:
        """Все аудиодорожки"""
        logger.info("get info about audio tracks")
        with open("track_info.json", "rb") as file:
            data = json.load(file)
        for i in data["tracks"]:
            if i.get("type") == "audio":
                track_id = i['id']
                codec = i['codec']
                language = i['properties']['language']
                try:
                    track_name = i['properties']['track_name']
                    track_info = {"id": f"id: {track_id}", "name": f"title: {track_name}", "codec": f"codec: {codec}",
                                  "language": f"language: {language}"}
                    print(track_info)
                except KeyError as exception:
                    logger.error(f"KeyError error: {exception}")
                    track_info = {"id": f"id: {track_id}", "codec": f"codec: {codec}",
                                  "language": f"language: {language}"}
                    print(track_info)

    @logger.catch
    def get_tracks_subtitles(self) -> None:
        """Все дорожки субтитров"""
        logger.info("get info about subtitles")
        with open("track_info.json", "rb") as file:
            data = json.load(file)
        for i in data["tracks"]:
            if i.get("type") == "subtitles":
                sub_id = i['id']
                language = i['properties']['language']
                try:
                    sub_name = i['properties']['track_name']
                    sub_info = {"id": f"id: {sub_id}", "name": f"title: {sub_name}", "language": f"language: {language}"}
                    print(sub_info)
                except KeyError as exception:
                    logger.error(f"KeyError error: {exception}")
                    sub_info = {"id": f"id: {sub_id}", "language": f"language: {language}"}
                    print(sub_info)

    @logger.catch
    def get_track_title_lang(self, track_id: int) -> dict:
        with open("track_info.json", "rb") as file:
            data = json.load(file)
        track_info = data["tracks"][track_id]
        track_lang = track_info["properties"]["language"]
        track_title = track_info["properties"]["track_name"]
        info = {"title": track_title, "lang": track_lang}
        return info

    @staticmethod
    @logger.catch
    def extract_track(mkv_path: str, track_id: int, temp_dir: str) -> None:
        """Извлечь аудиодорожку"""
        mkv_extract_path = r"I:\Python_Projects\MKVAudioCut\mkv_tools\mkvextract.exe"
        dts_path = rf"{track_id}:F:\test\temp\{temp_dir}\{track_id}.dts"
        logger.info(rf"starting extraction dts from {mkv_path}")
        subprocess.run([f"{mkv_extract_path}", "tracks", mkv_path, dts_path],
                       stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
        logger.info("dts extracted")

    @staticmethod
    @logger.catch
    def convert_to_ac3(track_id: int, temp_dir: str, bitrate: int = 640) -> str:
        ac3_converter = r"I:\Python_Projects\MKVAudioCut\eac3\eac3to.exe"
        dts_path = rf"F:\test\temp\{temp_dir}\{track_id}.dts"
        ac3_path = rf"F:\test\temp\{temp_dir}\{track_id}.ac3"
        logger.info(f"starting convert {track_id}.dts to {track_id}.ac3")
        subprocess.run([f"{ac3_converter}", dts_path, ac3_path, f"-{bitrate}", f"-down6"],
                       stdout=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        check_dts_path = os.path.exists(dts_path)
        if check_dts_path is True:
            os.remove(dts_path)
        logger.info(f"{track_id}.dts converted to {track_id}.ac3")
        return ac3_path

    @logger.catch
    def add_track_sub_to_mkv(self, mkv_path: str, output_path: str, sub_id: int | None, sub_path: str | None,
                             ac3_path: str, track_id: int) -> None:
        logger.info(f"starting build new mkv file")
        mkv_merge_path = r"I:\Python_Projects\MKVAudioCut\mkv_tools\mkvmerge.exe"
        track_metadata = self.get_track_title_lang(track_id)
        track_title = track_metadata.get("title")
        track_lang = track_metadata.get("lang")
        lang_name_command = f'--language 0:{track_lang} --track-name 0:"{track_title}"'
        if sub_id:
            sub_metadata = self.get_track_title_lang(sub_id)
            sub_title = sub_metadata.get("title")
            sub_lang = sub_metadata.get("lang")
            sub_command = f'--language 0:{sub_lang} --track-name 0:"{sub_title}"'
            logger.info(f"starting rebuilding with {ac3_path} sound and {sub_path} subtitles")
            subprocess.run(rf'{mkv_merge_path} -o {output_path} -A -S {mkv_path} {lang_name_command} {ac3_path} {sub_command} {sub_path}',
                           creationflags=subprocess.CREATE_NO_WINDOW)
            logger.info(f"mkv rebuilded")
        else:
            logger.info(f"starting rebuilding with {ac3_path} sound")
            subprocess.run(rf'{mkv_merge_path} -o {output_path} -A -S {mkv_path} {lang_name_command} {ac3_path}',
                           creationflags=subprocess.CREATE_NO_WINDOW)
            logger.info(f"mkv rebuilded")

    @logger.catch
    def extract_ac3(self, mkv_path: str, track_id: int, temp_dir: str) -> str:
        mkv_extract_path = r"I:\Python_Projects\MKVAudioCut\mkv_tools\mkvextract.exe"
        ac3_path_raw = rf"{track_id}:F:\test\temp\{temp_dir}\{track_id}.ac3"
        ac3_path = rf"F:\test\temp\{temp_dir}\{track_id}.ac3"
        logger.info(rf"starting extraction ac3 from {mkv_path}")
        subprocess.run([f"{mkv_extract_path}", "tracks", mkv_path, ac3_path_raw])
        logger.info("done")
        return ac3_path

    @logger.catch
    def extract_sub(self, mkv_path: str, sub_id: int, temp_dir: str) -> str:
        mkv_extract_path = r"I:\Python_Projects\MKVAudioCut\mkv_tools\mkvextract.exe"
        sub_path_raw = rf"{sub_id}:F:\test\temp\{temp_dir}\{sub_id}.srt"
        sub_path = rf"F:\test\temp\{temp_dir}\{sub_id}.srt"
        logger.info(rf"starting extraction subtitles from {mkv_path}")
        subprocess.run([f"{mkv_extract_path}", "tracks", mkv_path, sub_path_raw])
        logger.info("subtitles extracted")
        return sub_path

    @logger.catch
    def change_track_on_mkv(self, mkv_path: str, output_path: str, ac3_path: str, sub_path: str, track_id: int, sub_id: int):
        mkv_merge_path = r"I:\Python_Projects\MKVAudioCut\mkv_tools\mkvmerge.exe"
        track_metadata = self.get_track_title_lang(track_id)
        track_title = track_metadata.get("title")
        track_lang = track_metadata.get("lang")
        sub_metadata = self.get_track_title_lang(sub_id)
        sub_title = sub_metadata.get("title")
        sub_lang = sub_metadata.get("lang")
        lang_name_command = f'--language 0:{track_lang} --track-name 0:"{track_title}"'
        sub_command = f'--language 0:{sub_lang} --track-name 0:"{sub_title}"'
        logger.info(f"starting rebuilding mkv")
        subprocess.run(rf'{mkv_merge_path} -o {output_path} -A -S {mkv_path} {lang_name_command} {ac3_path} {sub_command} {sub_path}')
        logger.info(f"rebuild complete")

    @logger.catch
    def refactor_mkv(self) -> None:
        """Пересобрать mkv с 1 дорожкой ac3(без конвертации) и нужными субтитрами"""
        mkv_path = input("mkv path: ")
        output_path = input("new mkv path: ")
        self.get_mkv_info(mkv_path)
        self.get_tracks_audio()
        track = input("Track id: ")
        track_id = int(track)
        self.get_tracks_subtitles()
        sub = input("Sub id: ")
        sub_id = int(sub)
        temp_dir = generate_temp_dir()
        ac3_path = self.extract_ac3(mkv_path, track_id, temp_dir)
        sub_path = self.extract_sub(mkv_path, sub_id, temp_dir)
        self.change_track_on_mkv(mkv_path, output_path, ac3_path, sub_path, track_id, sub_id)
        os.remove("track_info.json")

    @logger.catch
    def start_rebuild_mkv(self) -> None:
        """Конвертирование 1 dts дорожки с выбором субтитров"""
        mkv_path = input("mkv path: ")
        output_path = input("new mkv path: ")
        self.get_mkv_info(mkv_path)
        self.get_tracks_audio()
        track = input("Track id: ")
        track_id = int(track)
        subtitles = input("subtitles Y/N?: ").lower()
        temp_dir = generate_temp_dir()
        if subtitles == "y" or subtitles == "yes":
            self.get_tracks_subtitles()
            sub = input("Sub id: ")
            sub_id = int(sub)
            sub_path = self.extract_sub(mkv_path, sub_id, temp_dir)
            self.extract_track(mkv_path, track_id, temp_dir)
            ac3_path = self.convert_to_ac3(track_id, temp_dir)
            self.add_track_sub_to_mkv(mkv_path, output_path, sub_id, sub_path, ac3_path, track_id)
            os.remove("track_info.json")
        else:
            self.extract_track(mkv_path, track_id, temp_dir)
            ac3_path = self.convert_to_ac3(track_id, temp_dir)
            self.add_track_sub_to_mkv(mkv_path, output_path, None, None, ac3_path, track_id)
            os.remove("track_info.json")



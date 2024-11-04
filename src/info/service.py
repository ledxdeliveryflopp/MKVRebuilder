import json
import subprocess
from dataclasses import dataclass

from loguru import logger

from static.mkv_tools.utils import get_mkv_tools_path


@dataclass
class MKVMergeService:
    """Сервис MKV Merge"""
    path = get_mkv_tools_path()
    mkv_merge_path: str = fr"{path}\mkvmerge.exe"

    @logger.catch
    def get_mkv_info(self, source_file: str) -> None:
        """Сбор информации о файле"""
        command = rf'-r track_info.json -J {source_file}'
        subprocess.run(rf"{self.mkv_merge_path} {command}", creationflags=subprocess.CREATE_NO_WINDOW)

    @logger.catch
    def build_sound_info(self) -> list:
        """Компановка информации о звуковых дорожках"""
        with open(f"track_info.json", 'rb') as file:
            data = json.load(file)
        info = []
        for i in data["tracks"]:
            if i.get("type") == "audio":
                audio_id = i['id']
                language = i['properties']['language']
                audio_codec = i['codec']
                try:
                    audio_name = i['properties']['track_name']
                    audio_info = {"id": f"{audio_id}", "format": f"{audio_codec}",
                                  "name": f"t{audio_name}", "language": f"{language}"}
                    info.append(audio_info)
                except KeyError:
                    audio_info = {"id": f"id: {audio_id}", "format": f"{audio_codec}",
                                  "language": f"{language}"}
                    info.append(audio_info)

        return info

    @logger.catch
    def build_subtitles_info(self) -> list:
        """Компановка информации о звуковых субтитрах"""
        with open(f"track_info.json", 'rb') as file:
            data = json.load(file)
        info = []
        for i in data["tracks"]:
            if i.get("type") == "subtitles":
                sub_id = i['id']
                language = i['properties']['language']
                try:
                    sub_name = i['properties']['track_name']
                    sub_info = {"id": f"{sub_id}", "name": f"{sub_name}",
                                "language": f"{language}"}
                    info.append(sub_info)
                except KeyError:
                    sub_info = {"id": f"{sub_id}", "language": f"{language}"}
                    info.append(sub_info)

        return info


def init_mkv_merge_service() -> MKVMergeService:
    return MKVMergeService()


mkv_merge_service = init_mkv_merge_service()

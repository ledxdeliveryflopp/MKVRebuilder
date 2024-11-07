import os
import random
import string

from loguru import logger


@logger.catch
def generate_temp_dir(temp_path: str, track_id: int, sub_id: int | None) -> dict:
    temp_dir_list = random.choices(string.octdigits, k=8)
    temp_dir_str = ''.join(temp_dir_list)
    os.makedirs(f"{temp_path}/temp/{temp_dir_str}/")
    if sub_id:
        sound_temp_dir_id = f"{track_id}:{temp_path}/temp/{temp_dir_str}/"
        subtitle_temp_dir_id = f"{sub_id}:{temp_path}/temp/{temp_dir_str}/"
        sound_temp_dir = f"{temp_path}/temp/{temp_dir_str}/"
        subtitle_temp_dir = f"{temp_path}/temp/{temp_dir_str}/"
        return {"sound_id": sound_temp_dir_id, "sub_id": subtitle_temp_dir_id,
                "sound": sound_temp_dir, "sub": subtitle_temp_dir}
    else:
        sound_temp_dir_id = f"{track_id}:{temp_path}/temp/{temp_dir_str}/"
        sound_temp_dir = f"{temp_path}/temp/{temp_dir_str}/"
        return {"sound_id": sound_temp_dir_id, "sound": sound_temp_dir}


@logger.catch
def clear_temp_dts(dts_path: str) -> None:
    """Удаление dts из временной папки"""
    try:
        os.remove(dts_path)
        logger.info(f"dts remove")
    except Exception as exception:
        logger.error(f"clear_temp_dts - {exception}")


@logger.catch
def clear_temp_ac3(ac3_path: str) -> None:
    """Удаление ac3 из временной папки"""
    os.remove(ac3_path)
    logger.info(f"ac3 remove")


@logger.catch
def clear_temp_eac3(eac3_path: str) -> None:
    """Удаление eac3 из временной папки"""
    os.remove(eac3_path)
    logger.info(f"eac3 remove")


@logger.catch
def clear_temp_srt(srt_path: str) -> None:
    """Удаление srt из временной папки"""
    os.remove(srt_path)
    logger.info(f"srt remove")

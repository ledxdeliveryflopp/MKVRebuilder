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


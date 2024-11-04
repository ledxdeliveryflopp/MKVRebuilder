import os


def get_mkv_tools_path() -> str:
    """Местоположение mkv tools"""
    mkv_tools_path = os.path.dirname(os.path.realpath(__file__))
    return mkv_tools_path

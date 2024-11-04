import os


def get_eac3_path() -> str:
    """Местоположение eac3"""
    path = os.path.dirname(os.path.realpath(__file__))
    return path

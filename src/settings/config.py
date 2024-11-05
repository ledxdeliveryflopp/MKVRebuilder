import configparser
import os
from dataclasses import dataclass

from loguru import logger


@dataclass
class IniConfig:
    """Класс ini настроек приложения"""
    config = configparser.ConfigParser()

    @logger.catch
    def set_base_ini_config(self) -> None:
        """Создание базового конфига"""
        path = os.path.exists("config/config.ini")
        if path is False:
            os.makedirs(rf"{os.getcwd()}\config")
            self.config["DIRS"] = {"temp": ""}
            with open("config/config.ini", "w") as file:
                self.config.write(file)

    @logger.catch
    def get_temp_dir(self) -> str | None:
        """Путь к временной директории"""
        self.config.read("config/config.ini")
        if "DIRS" in self.config:
            temp_path = self.config["DIRS"]["temp"]
            if temp_path:
                return temp_path
        else:
            return None

    @logger.catch
    def change_temp_dir_section(self, temp_dir: str) -> None:
        path = os.path.exists("config/config.ini")
        self.config["DIRS"] = {"temp": temp_dir}
        if path is True:
            with open("config/config.ini", "w") as file:
                self.config.write(file)
        else:
            self.set_base_ini_config()
            with open("config/config.ini", "w") as file:
                self.config.write(file)

def init_ini_settings() -> IniConfig:
    return IniConfig()


ini_settings = init_ini_settings()

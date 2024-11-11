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
        ini_path = os.path.exists("config/config.ini")
        dir_path = os.path.exists(rf"{os.getcwd()}\config")
        if dir_path is False:
            os.makedirs(rf"{os.getcwd()}\config")
            self.config["DIRS"] = {"temp": "", "output": ""}
            with open("config/config.ini", "w") as file:
                self.config.write(file)
        elif ini_path is False:
            self.config["DIRS"] = {"temp": "", "output": ""}
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
    def get_output_dir(self) -> str | None:
        """Путь к директории сохранения mkv"""
        self.config.read("config/config.ini")
        if "DIRS" in self.config:
            output_path = self.config["DIRS"]["output"]
            if output_path:
                return output_path
        else:
            return None

    @logger.catch
    def change_temp_dir_section(self, temp_dir: str) -> None:
        path = os.path.exists("config/config.ini")
        if path is True:
            self.config.set('DIRS', 'temp', temp_dir)
            with open('config/config.ini', 'w') as config_file:
                self.config.write(config_file)
        else:
            self.set_base_ini_config()
            self.config.set('DIRS', 'temp', temp_dir)
            with open('config/config.ini', 'w') as config_file:
                self.config.write(config_file)

    @logger.catch
    def change_output_dir_section(self, output_dir: str) -> None:
        path = os.path.exists("config/config.ini")
        if path is True:
            self.config.set('DIRS', 'output', output_dir)
            with open('config/config.ini', 'w') as config_file:
                self.config.write(config_file)
        else:
            self.set_base_ini_config()
            self.config.set('DIRS', 'output', output_dir)
            with open('config/config.ini', 'w') as config_file:
                self.config.write(config_file)


def init_ini_settings() -> IniConfig:
    return IniConfig()


ini_settings = init_ini_settings()

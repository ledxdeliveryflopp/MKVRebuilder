from dataclasses import dataclass


@dataclass
class Settings:
    """Настройки приложения"""
    black_theme: bool = False
    debug_mode: bool = False

    def get_debug_status(self) -> bool:
        """Получить статус дебаг режима"""
        return self.debug_mode

    def get_theme_status(self) -> bool:
        """Получить статус темной темы"""
        return self.black_theme

    def change_theme(self, status: bool) -> None:
        """Изменить тему на темную"""
        self.black_theme = status


def init_settings() -> Settings:
    return Settings()


settings = init_settings()

from dataclasses import dataclass


@dataclass
class Settings:
    """Настройки приложения"""
    black_theme: bool = False
    profiler_status: bool = False

    @property
    def get_profiler_status(self) -> bool:
        """Получить статус режима профилирования"""
        return self.profiler_status

    def change_profiler_status(self, status: bool) -> None:
        """Изменить статус профилирования"""
        self.profiler_status = status

    def get_theme_status(self) -> bool:
        """Получить статус темной темы"""
        return self.black_theme

    def change_theme(self, status: bool) -> None:
        """Изменить тему на темную"""
        self.black_theme = status


def init_settings() -> Settings:
    return Settings()


settings = init_settings()

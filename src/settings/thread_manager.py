from dataclasses import dataclass

from PySide6.QtCore import QThreadPool


@dataclass
class ThreadManager:
    """Менеджен потоков"""
    thread_manager = QThreadPool()

    def get_active_thread_count(self) -> int:
        """Возврат колличества активных потоков"""
        return self.thread_manager.activeThreadCount()

    def get_max_thread_count(self) -> int:
        """Возврат колличества доступных потоков в ЦП"""
        return self.thread_manager.maxThreadCount()

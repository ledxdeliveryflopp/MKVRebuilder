import time
from dataclasses import dataclass

import psutil
from PySide6.QtCore import QThreadPool, Signal, QThread


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


class DebugThread(QThread):
    """Поток для дебага"""
    cpu_disc_usage_signal = Signal(str)

    def __init__(self, disc: str) -> None:
        super().__init__()
        self.disc = disc

    def run(self) -> None:
        """Подсчет использования CPU и диска"""
        while True:
            cpu_usage = psutil.cpu_percent()
            disc_usage = psutil.disk_usage(self.disc)
            disc_free = round(disc_usage.free / (1024 ** 3), 1)
            disc_percent = disc_usage[3]
            time.sleep(5)
            self.cpu_disc_usage_signal.emit(f"Cpu usage: {cpu_usage}%, Disk free: {disc_free}GB,"
                                            f" Disk usage: {disc_percent}%")

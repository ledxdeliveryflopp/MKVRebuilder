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


class GetCpuUsageThread(QThread):
    cpu_usage_signal = Signal(str)

    def __init__(self):
        super().__init__()

    def get_cpu_usage(self):
        while True:
            usage = psutil.cpu_percent()
            time.sleep(2)
            self.cpu_usage_signal.emit(f"Cpu usage: {usage}%")

    def run(self):
        while True:
            usage = psutil.cpu_percent()
            time.sleep(2)
            self.cpu_usage_signal.emit(f"Cpu usage: {usage}%")

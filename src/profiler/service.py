import psutil
from PySide6.QtCore import Signal, QThread
from loguru import logger
from psutil import NoSuchProcess


class ProfilerThread(QThread):
    """Поток для профилировация подпроцессов"""
    profiler_signal = Signal(str)

    def __init__(self, process_id: int) -> None:
        super().__init__()
        self.process_id: int = process_id

    @logger.catch
    def profile_subprocess_usage(self) -> None:
        """Подсчет использования mkvmerge/mkvextract/eac3to CPU/RAM и операций ввода-вывода"""
        logger.debug(f"start profiling process with id: {self.process_id}")
        while self.isRunning() is True:
            try:
                process = psutil.Process(self.process_id)
                with process.oneshot():
                    name = process.name()
                    cpu_percent = format(process.cpu_percent(interval=1) / psutil.cpu_count(), ".1f")
                    ram_usage_mb = format(process.memory_info()[0] / (1024 ** 2), ".1f")
                    io_read = process.io_counters()[0]
                    io_write = process.io_counters()[1]
                self.profiler_signal.emit(f"process: {name}, cpu usage: {cpu_percent}%, ram usage: {ram_usage_mb}mb, "
                                          f"io read: {io_read}, io write: {io_write}")
            except NoSuchProcess as exception:
                self.finished.emit()

    @logger.catch
    def run(self) -> None:
        """Запуск потока"""
        self.profile_subprocess_usage()

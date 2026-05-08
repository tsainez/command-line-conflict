"""Performance profiler utility."""

import csv
import functools
import time
import tracemalloc
from datetime import datetime

from .. import config
from .paths import get_user_data_dir


class Profiler:
    """A singleton profiler to track frame times, frame drops, and memory usage."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self) -> None:
        self.enabled = getattr(config, "DEV_MODE", False)
        if self.enabled:
            tracemalloc.start()

        self.metrics_buffer = []
        self.frame_count = 0
        self.total_time = 0.0
        self.fps = 0.0
        self.frame_drops = 0
        self.csv_path = None
        self.last_flush_time = time.time()

        if self.enabled:
            log_dir = get_user_data_dir()
            log_dir.mkdir(parents=True, exist_ok=True)
            self.csv_path = log_dir / f"profiler_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Timestamp", "FrameTime", "FrameDrop", "MemoryUsageMB", "FunctionName", "ExecTime"])

    def record_frame(self, dt: float) -> None:
        if not self.enabled:
            return

        self.frame_count += 1
        self.total_time += dt

        target_frame_time = 1.0 / config.FPS if config.FPS > 0 else 0
        frame_drop = 0
        # If frame took longer than target + 10%, we count it as a drop
        if dt > target_frame_time * 1.1:
            frame_drop = 1
            self.frame_drops += 1

        if self.total_time >= 1.0:
            self.fps = self.frame_count / self.total_time
            self.frame_count = 0
            self.total_time = 0.0

        current, _ = tracemalloc.get_traced_memory()
        mem_mb = current / (1024 * 1024)

        self.log_metric("Frame", dt, frame_drop, mem_mb)

    def log_metric(self, func_name: str, exec_time: float, frame_drop: int = 0, mem_mb: float = -1.0) -> None:
        if not self.enabled:
            return

        if mem_mb < 0.0:
            current, _ = tracemalloc.get_traced_memory()
            mem_mb = current / (1024 * 1024)

        timestamp = datetime.now().isoformat()
        self.metrics_buffer.append([timestamp, f"{exec_time:.6f}", frame_drop, f"{mem_mb:.2f}", func_name, f"{exec_time:.6f}"])

        # Flush every second
        current_time = time.time()
        if current_time - self.last_flush_time >= 1.0:
            self.flush()
            self.last_flush_time = current_time

    def flush(self) -> None:
        if not self.enabled or not self.csv_path or not self.metrics_buffer:
            return

        with open(self.csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.metrics_buffer)
        self.metrics_buffer.clear()

    def get_stats(self) -> dict:
        """Returns current stats for the developer console."""
        if not self.enabled:
            return {"fps": 0.0, "frame_drops": 0, "memory_mb": 0.0}

        current, _ = tracemalloc.get_traced_memory()
        mem_mb = current / (1024 * 1024)
        return {
            "fps": self.fps,
            "frame_drops": self.frame_drops,
            "memory_mb": mem_mb
        }


profiler = Profiler()


def profile(func):
    """Decorator to profile execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not profiler.enabled:
            return func(*args, **kwargs)

        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        exec_time = end_time - start_time

        profiler.log_metric(func.__name__, exec_time)
        return result
    return wrapper

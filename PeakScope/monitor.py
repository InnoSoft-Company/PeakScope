"""Function monitoring with per-function CPU / RAM / time reporting."""

import time as tm
import tracemalloc

class Monitor:
    def __init__(self, func, cpu=True, ram=True, measure_time=True):
        self.func = func
        self.cpu = cpu
        self.ram = ram
        self.measure_time = measure_time

    def run(self, *args, **kwargs):
        start_time = tm.perf_counter() if self.measure_time else None
        start_cpu = tm.process_time() if self.cpu else None

        if self.ram:
            tracemalloc.start()

        try:
            result = self.func(*args, **kwargs)
        finally:
            if self.ram:
                current_mem, peak_mem = tracemalloc.get_traced_memory()
                tracemalloc.stop()

        end_time = tm.perf_counter() if self.measure_time else None
        end_cpu = tm.process_time() if self.cpu else None

        report = {}

        if self.measure_time:
            report["wall_time"] = end_time - start_time

        if self.cpu:
            report["cpu_time"] = end_cpu - start_cpu

        if self.ram:
            report["current_ram"] = current_mem / (1024 * 1024)
            report["peak_ram"] = peak_mem / (1024 * 1024)

        return result, report
"""Function monitoring with per-function CPU / RAM / time reporting."""

import time as tm
import psutil

proc = psutil.Process()

class Monitor:
    """Monitor function execution time, CPU and RAM usage."""
    
    def __init__(self, func, cpu=True, ram=True, time=True):
        self.func = func
        self.cpu = cpu
        self.ram = ram
        self.time = time
    
    def run(self, *args, **kwargs):
        """Run the monitored function and report CPU, RAM and time usage."""
        start_time = tm.perf_counter() if self.time else None
        cpu_start = proc.cpu_times().user + proc.cpu_times().system if self.cpu or self.ram else None
        rss_start = proc.memory_info().rss if self.ram else None
        
        try:
            result = self.func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred while executing function: {e}")
            raise

        end_time = tm.perf_counter() if self.time else None
        cpu_end = (proc.cpu_times().user + proc.cpu_times().system) if self.cpu else None
        ram_end = (proc.memory_info().rss) if self.ram else None
        
        time_taken = (end_time - start_time) if self.time else None
        cpu_usage = ((cpu_end - cpu_start) / time_taken * 100) if self.cpu and time_taken else None
        ram_usage = ((ram_end - rss_start) / (1024 * 1024)) if self.ram else None  # Convert bytes to MB
        
        report = {}
        
        if self.time:
            report['time'] = f"{end_time - start_time:.4f} seconds"
        if self.cpu:
            report['cpu'] = f"{cpu_usage:.2f}%"
        if self.ram:
            report['ram'] = f"{ram_usage:.2f} MB"
        
        return f"func results: {result}", report
import platform
import psutil
import humanize

from typing import Dict
from dataclasses import dataclass

KNOWN_TEMP_SENSOR_NAMES = ["cpu_thermal", "coretemp"]

def h(val: int, binary=True) -> str:
    return humanize.naturalsize(val, binary)


@dataclass
class SystemSample:
    host_name: str = ""

    num_cores: int = -1
    cpu_percent: float = 0.0

    mem_total: int = -1
    mem_used: int = -1
    mem_free: int = -1
    mem_percent: float = 0.0

    swap_total: int = -1
    swap_used: int = -1
    swap_free: int = -1
    swap_percent: float = 0.0

    disk_used: int = -1

    cpu_temp: float = 0.0


    def to_dict(self) -> Dict:
        return {
            "host_name": self.host_name,
            "num_cores": self.num_cores,
            "cpu_percent": self.cpu_percent,
            "mem_total": self.mem_total,
            "mem_used": self.mem_used,
            "mem_free": self.mem_free,
            "mem_percent": self.mem_percent,
            "swap_total": self.swap_total,
            "swap_used": self.swap_used,
            "swap_free": self.swap_free,
            "swap_percent": self.swap_percent,
            "disk_used": self.disk_used,
            "cpu_temp": self.cpu_temp,
        }

    def __str__(self):
        hmt = h(self.mem_total)
        hmu = h(self.mem_used)
        hmf = h(self.mem_free)

        hst = h(self.swap_total)
        hsu = h(self.swap_used)
        hsf = h(self.swap_free)

        hdu = h(self.disk_used)

        m = f"HOST: {self.host_name}\n" \
            f"CPU: cores {self.num_cores}, load: {self.cpu_percent}%, temp: {self.cpu_temp} C, \n" \
            f"MEM: total {hmt}, used {hmu}, free {hmf}, percent {self.mem_percent}%\n" \
            f"SWAP: total {hst}, used {hsu}, free {hsf} percent {self.swap_percent}%\n" \
            f"DISK: used {hdu}"

        return m


class SystemSampler:

    def __init__(self):
        self.last_sample = None
        self.num_cores = psutil.cpu_count(False)
        self.mem_total = psutil.virtual_memory().total
        self.swap_total = psutil.swap_memory().total
        self.host_name = platform.uname().node


    def get_current_sample(self, _path="/"):
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disk = psutil.disk_usage(_path)
        temp = {k: max([t.current for t in v]) for k, v in psutil.sensors_temperatures().items()}
        try:
            cpu_temp = max([v for k, v in temp.items() if k in KNOWN_TEMP_SENSOR_NAMES])
        except ValueError:
            cpu_temp = max(temp.values()) if temp.values() else 0.0

        return SystemSample(self.host_name,
                            self.num_cores, psutil.cpu_percent(),
                            self.mem_total, mem.used, mem.free, mem.percent,
                            self.swap_total, swap.used, swap.free, swap.percent,
                            disk.used, cpu_temp=cpu_temp)

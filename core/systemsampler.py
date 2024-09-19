import humanize
import platform
import psutil
import time

from collections import namedtuple
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from psutil._common import snetio

KNOWN_TEMP_SENSOR_NAMES = ["cpu_thermal", "coretemp"]
NET_HISTORY_DURATION = 60

def h(val: Union[int, float], binary=True) -> str:
    return humanize.naturalsize(val, binary)

@dataclass
class NetSample:
    timestamp: float
    sent: int
    received: int


@dataclass
class NetRates:
    upload: float
    download: float


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

    net_upload: float = 0.0
    net_download: float = 0.0

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
            "net_upload": self.net_upload,
            "net_download": self.net_download,
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
            f"DISK: used {hdu}\n" \
            f"NET: upload {h(self.net_upload)}/s, download {h(self.net_download)}/s"

        return m


class SystemSampler:

    def __init__(self):
        self.num_cores = psutil.cpu_count(False)
        self.mem_total = psutil.virtual_memory().total
        self.swap_total = psutil.swap_memory().total
        self.host_name = platform.uname().node

        self.last_net: Optional[snetio] = None
        self.net_history: List[NetSample] = []

    def _save_net_history(self, sent: int, recv: int):
        now = time.time()
        self.net_history = [v for v in self.net_history if v.timestamp + NET_HISTORY_DURATION > now]
        self.net_history.append(NetSample(now, sent, recv))

    def _get_net_rates(self) -> NetRates:
        min_timestamp = None
        max_timestamp = None
        upload = 0
        download = 0

        for v in self.net_history:
            if not min_timestamp:
                min_timestamp = v.timestamp
            max_timestamp = v.timestamp
            upload += v.sent
            download += v.received

        if min_timestamp and max_timestamp:
            interval = max_timestamp - min_timestamp
            if interval > 0:
                return NetRates(upload / interval, download / interval)

        return NetRates(0.0, 0.0)

    def get_current_sample(self, _path="/"):
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disk = psutil.disk_usage(_path)

        temp = {k: max([t.current for t in v]) for k, v in psutil.sensors_temperatures().items()}
        try:
            cpu_temp = max([v for k, v in temp.items() if k in KNOWN_TEMP_SENSOR_NAMES])
        except ValueError:
            cpu_temp = max(temp.values()) if temp.values() else 0.0

        net = psutil.net_io_counters()
        self._save_net_history(
            sent=net.bytes_sent - self.last_net.bytes_sent if self.last_net else 0,
            recv=net.bytes_recv - self.last_net.bytes_recv if self.last_net else 0,
        )
        self.last_net = net

        net_rates = self._get_net_rates()

        sample = SystemSample(
            host_name=self.host_name,
            num_cores=self.num_cores,
            cpu_percent=psutil.cpu_percent(),
            mem_total=self.mem_total,
            mem_used=mem.used,
            mem_free=mem.free,
            mem_percent=mem.percent,
            swap_total=self.swap_total,
            swap_used=swap.used,
            swap_free=swap.free,
            swap_percent=swap.percent,
            disk_used=disk.used,
            cpu_temp=cpu_temp,
            net_upload=net_rates.upload,
            net_download=net_rates.download,
        )
        return sample

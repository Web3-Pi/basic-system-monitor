import time
from threading import Thread

from config.conf import SYSTEM_STATS_UPDATE_INTERVAL, DEFAULT_PATH
from core.systemsampler import SystemSampler, SystemSample


class SystemMonitor(Thread):

    def __init__(self, update_interval: float = SYSTEM_STATS_UPDATE_INTERVAL, _path: str = DEFAULT_PATH) -> None:
        super().__init__(daemon=True)

        self.update_interval = update_interval
        self.path = _path

        self.quit = False

        self.sampler = SystemSampler()
        self.last_sample = self.sampler.get_current_sample(self.path)

    def start(self) -> None:
        super().start()

    def _sample_system(self) -> None:
        self.last_sample = self.sampler.get_current_sample(self.path)

    def run(self):
        print("Starting system monitor service")

        while not self.quit:
            time.sleep(self.update_interval)
            self._sample_system()

        print("Stopping system monitor service")

    def get_last_sample(self) -> SystemSample:
        return self.last_sample

    def stop(self) -> None:
        self.quit = True
        self.join()

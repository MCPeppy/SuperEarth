########## super_earth/sdr/rtl433.py ##########
"""Subprocess stub that emits fake rtl_433 JSON lines."""
from __future__ import annotations

import json
import random
import time
from super_earth.threads import TkThread

class Rtl433Thread(TkThread):
    def __init__(self, tk_root, queue):
        super().__init__(tk_root)
        self.queue = queue

    def run(self):
        while not self.stopping:
            msg = {
                "model": "MockTempSensor",
                "temperature_C": round(random.uniform(18, 26), 1),
                "humidity": random.randint(30, 70),
                "time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            self.safe_callback(self.queue.put, msg)
            time.sleep(5)

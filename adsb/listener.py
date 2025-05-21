########## super_earth/adsb/listener.py ##########
"""Mock ADS‑B socket listener – generates fake flights."""
from __future__ import annotations

import random
import time
from super_earth.threads import TkThread

class AdsbListener(TkThread):
    CALLSIGNS = ["UAL123", "DAL456", "AAL789", "N42KR", "JBU101"]

    def __init__(self, tk_root, queue):
        super().__init__(tk_root)
        self.queue = queue

    def run(self):
        while not self.stopping:
            plane = {
                "flight": random.choice(self.CALLSIGNS),
                "alt": random.randint(2000, 38000),
                "speed": random.randint(120, 520)
            }
            self.safe_callback(self.queue.put, plane)
            time.sleep(3)

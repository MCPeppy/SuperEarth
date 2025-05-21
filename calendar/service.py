########## super_earth/calendar/service.py ##########
"""Minimal Google Calendar polling stub (mock)."""
from __future__ import annotations

import datetime as _dt
from super_earth.threads import TkThread

# Real implementation will import google‑api‑python‑client.

def _mock_events(n: int = 5):
    now = _dt.datetime.utcnow()
    return [
        {
            "start": (now + _dt.timedelta(hours=i)).strftime("%Y-%m-%d %H:%M"),
            "summary": f"Mock Event {i+1}"
        }
        for i in range(n)
    ]

class CalendarService(TkThread):
    """Background thread – fetch events every 10 min and push to UI queue."""

    POLL_SEC = 600

    def __init__(self, tk_root, queue):
        super().__init__(tk_root)
        self.queue = queue

    def run(self):
        while not self.stopping:
            events = _mock_events()  # TODO replace with real API call
            self.safe_callback(self.queue.put, events)
            self._stop_event.wait(self.POLL_SEC)

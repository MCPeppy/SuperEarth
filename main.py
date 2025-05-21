########## super_earth/main.py ##########
"""Entry point that wires everything together."""
from __future__ import annotations

import queue
import tkinter as tk
from tkinter import ttk

from super_earth.ui.dashboard import Dashboard
from super_earth.calendar.panel import CalendarPanel
from super_earth.calendar.service import CalendarService
from super_earth.camera.panel import CameraPanel
from super_earth.camera.feed import CameraFeed
from super_earth.sdr.panel import RadioPanel
from super_earth.sdr.rtl433 import Rtl433Thread
from super_earth.adsb.panel import AircraftPanel
from super_earth.adsb.listener import AdsbListener


def run():
    root = tk.Tk()
    root.state("zoomed")  # maximise on Windows

    dashboard = Dashboard(root)

    # Instantiate panels ---------------------------------------------------
    cam_panel = CameraPanel(dashboard.camera_frame)
    cam_panel.pack(fill="both", expand=True)

    cal_panel = CalendarPanel(dashboard.calendar_frame)
    cal_panel.pack(fill="both", expand=True)

    radio_panel = RadioPanel(dashboard.radio_frame)
    radio_panel.pack(fill="both", expand=True)

    aircraft_panel = AircraftPanel(dashboard.aircraft_frame)
    aircraft_panel.pack(fill="both", expand=True)

    # Queues
    cal_q: queue.Queue = queue.Queue()
    radio_q: queue.Queue = queue.Queue()
    adsb_q: queue.Queue = queue.Queue()

    # Worker threads -------------------------------------------------------
    CalendarService(root, cal_q).start()
    CameraFeed(root, cam_panel.draw).start()
    Rtl433Thread(root, radio_q).start()
    AdsbListener(root, adsb_q).start()

    # Periodic queue polling ----------------------------------------------
    def poll_queues():
        while True:
            try:
                evts = cal_q.get_nowait()
                cal_panel.update_events(evts)
            except queue.Empty:
                break
        while True:
            try:
                msg = radio_q.get_nowait()
                radio_panel.append(msg)
            except queue.Empty:
                break
        while True:
            try:
                plane = adsb_q.get_nowait()
                aircraft_panel.upsert(plane)
            except queue.Empty:
                break
        root.after(200, poll_queues)  # 5×/sec

    poll_queues()
    root.mainloop()

if __name__ == "__main__":
    run()

# =============================================================
# End of skeleton. Real integrations (cv2, Google API, rtl_433,
# dump1090, TkinterMapView) replace the mock stubs above.
# =============================================================

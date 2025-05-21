########## super_earth/camera/feed.py ##########
"""Camera capture thread – uses OpenCV. Here returns a blank image."""
from __future__ import annotations

import time
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

from super_earth.threads import TkThread

class CameraFeed(TkThread):
    def __init__(self, tk_root: tk.Tk, draw_callback):
        super().__init__(tk_root)
        self.draw_callback = draw_callback

    def run(self):
        # Mock loop – replace with cv2.VideoCapture
        counter = 0
        while not self.stopping:
            img = self._make_placeholder_frame(counter)
            self.safe_callback(self.draw_callback, img)
            counter += 1
            time.sleep(1 / 10)  # 10 FPS

    @staticmethod
    def _make_placeholder_frame(i):
        im = Image.new("RGB", (640, 360), "black")
        d = ImageDraw.Draw(im)
        d.text((10, 10), f"Camera frame {i}", fill="white")
        return ImageTk.PhotoImage(im)

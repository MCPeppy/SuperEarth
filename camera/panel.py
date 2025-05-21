########## super_earth/camera/panel.py ##########
"""Tk widget that displays the live camera frame."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

class CameraPanel(ttk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)
        self.label = ttk.Label(self)
        self.label.pack(fill="both", expand=True)

    def draw(self, image):
        self.label.configure(image=image)
        self.label.image = image  # prevent GC

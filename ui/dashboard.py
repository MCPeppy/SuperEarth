########## super_earth/ui/dashboard.py ##########
"""Tkinter layout manager for the main dashboard."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

class Dashboard(ttk.Frame):
    """Grid‑based layout with references to feature panels."""

    def __init__(self, master: tk.Tk):
        super().__init__(master)
        master.title("SuperEarth Family Hub")
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure((0, 1, 2), weight=1)

        # Top – Camera -----------------------------------------------------
        self.camera_frame = ttk.Frame(self, relief="sunken")
        self.camera_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.camera_frame.configure(height=master.winfo_screenheight() * 0.4)

        # Bottom – Calendar, Radio, Aircraft ------------------------------
        self.calendar_frame = ttk.Frame(self, relief="ridge")
        self.radio_frame = ttk.Frame(self, relief="ridge")
        self.aircraft_frame = ttk.Frame(self, relief="ridge")

        for idx, frame in enumerate(
            (self.calendar_frame, self.radio_frame, self.aircraft_frame)
        ):
            frame.grid(row=1, column=idx, sticky="nsew")
            master.grid_columnconfigure(idx, weight=1)

        self.pack(fill="both", expand=True)

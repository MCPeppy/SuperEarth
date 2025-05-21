########## super_earth/calendar/panel.py ##########
"""Tk widget that shows upcoming events."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

class CalendarPanel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="Family Calendar", font=("Segoe UI", 16, "bold"))\
            .pack(anchor="w")
        self.tree = ttk.Treeview(self, columns=("when", "what"), show="headings")
        self.tree.heading("when", text="When")
        self.tree.heading("what", text="What")
        self.tree.pack(fill="both", expand=True)

    def update_events(self, events):
        self.tree.delete(*self.tree.get_children())
        for ev in events:
            self.tree.insert("", "end", values=(ev["start"], ev["summary"]))

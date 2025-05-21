########## super_earth/adsb/panel.py ##########
from __future__ import annotations

from tkinter import ttk

class AircraftPanel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.tree = ttk.Treeview(self, columns=("alt", "spd"), show="headings")
        self.tree.heading("alt", text="Alt ft")
        self.tree.heading("spd", text="Speed kt")
        self.tree.pack(fill="both", expand=True)
        self.rows = {}

    def upsert(self, plane):
        pk = plane["flight"]
        if pk in self.rows:
            self.tree.item(self.rows[pk], values=(plane["alt"], plane["speed"]))
        else:
            item = self.tree.insert("", "end", values=(plane["alt"], plane["speed"]))
            self.tree.item(item, tags=(pk,))
            self.rows[pk] = item

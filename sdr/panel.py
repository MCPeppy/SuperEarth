########## super_earth/sdr/panel.py ##########
"""Scrollable text log showing rtl_433 messages."""
import tkinter as tk
from tkinter import ttk
import json

class RadioPanel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.text = tk.Text(self, state="disabled", height=15)
        self.text.pack(fill="both", expand=True)

    def append(self, msg_dict):
        self.text.configure(state="normal")
        self.text.insert("end", json.dumps(msg_dict) + "\n")
        self.text.configure(state="disabled")
        self.text.see("end")

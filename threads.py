########## super_earth/threads.py ##########
"""Thread helper that guarantees safe GUI callbacks."""
from __future__ import annotations

import queue
import threading
import tkinter as tk
from typing import Callable

Callback = Callable[..., None]

class TkThread(threading.Thread):
    """Background thread that can *schedule* a callback on the Tk mainloop."""

    def __init__(self, tk_root: tk.Tk, *a, **kw):
        super().__init__(*a, **kw, daemon=True)
        self._tk_root = tk_root
        self._stop_event = threading.Event()

    # ---------------------------------------------------------------------
    def safe_callback(self, fn: Callback, *a, **kw):
        """Execute *fn* on the main thread via `root.after(0, ...)`."""
        self._tk_root.after(0, lambda: fn(*a, **kw))

    # ---------------------------------------------------------------------
    def stop(self):
        """Signal the worker loop to exit cleanly."""
        self._stop_event.set()

    @property
    def stopping(self) -> bool:  # convenience for subclasses
        return self._stop_event.is_set()

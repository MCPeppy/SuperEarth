########## super_earth/config.py ##########
"""Centralised configuration loader.

Reads *settings.yaml* at startup and exposes a **singleton**
`Settings` object so that every module shares the same config.
"""
from __future__ import annotations

import pathlib
import typing as _t
import yaml

_CONFIG_PATH = pathlib.Path(__file__).with_suffix(".yaml").parent / "settings.yaml"

class Settings:
    """Read‑only wrapper so accidental writes raise AttributeError."""

    def __init__(self, data: dict[str, _t.Any]):
        self._data = data

    def __getattr__(self, item):  # noqa: DunderMethod
        try:
            return self._data[item]
        except KeyError:
            raise AttributeError(item) from None

    # Convenience accessors --------------------------------------------------
    @property
    def camera_urls(self) -> list[str]:
        return self._data.get("camera_urls", [])

    @property
    def calendar_id(self) -> str | None:
        return self._data.get("calendar_id")

    @property
    def property_latlon(self) -> tuple[float, float]:
        return tuple(self._data.get("property_latlon", (0.0, 0.0)))

# Lazy‑loaded singleton instance
_settings: Settings | None = None

def get_settings() -> Settings:
    """Return the cached `Settings` instance; load on first call."""
    global _settings  # noqa: PLW0603
    if _settings is None:
        try:
            data = yaml.safe_load(_CONFIG_PATH.read_text())
        except FileNotFoundError:
            raise FileNotFoundError(
                f"settings.yaml not found at {_CONFIG_PATH}; copy settings.example.yaml"
            )
        _settings = Settings(data)
    return _settings

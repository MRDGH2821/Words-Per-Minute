"""Words Per Minute - A speed reading training application.

This package provides a fullscreen words-per-minute reading trainer
with customizable speed and display settings.
"""

from .app import WPMApp, main
from .config import AppConfig
from .core import WordReader
from .ui import WPMWindow

__version__ = "1.0.1"
__all__ = ["WPMApp", "main", "AppConfig", "WordReader", "WPMWindow"]
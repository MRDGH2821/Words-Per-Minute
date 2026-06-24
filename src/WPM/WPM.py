"""Words per minute - Legacy entry point.

This module provides backwards compatibility by wrapping the new modular structure.
For new code, please use: from WPM import WPMApp, main

Version - 1.0.1
"""

# Import the modern implementation
from .app import main

# For backwards compatibility, expose main at module level
__all__ = ["main"]

if __name__ == "__main__":
    main()
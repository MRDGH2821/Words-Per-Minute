"""Main application module for Words Per Minute.

This module provides the main application class that coordinates
configuration, word reading, and UI components.
"""

import os
import sys
from pathlib import Path
from typing import Optional

# Fix XWayland threading issues BEFORE importing tkinter
# This must happen before any GUI libraries are loaded
def _init_x11_threading():
    """Initialize X11 threading support for XWayland compatibility."""
    wayland_display = os.environ.get('WAYLAND_DISPLAY')
    xdg_session = os.environ.get('XDG_SESSION_TYPE')
    
    if wayland_display or xdg_session == 'wayland':
        try:
            # Call XInitThreads before any X11 operations
            import ctypes
            import ctypes.util
            
            # Find and load libX11
            x11_lib = ctypes.util.find_library('X11')
            if x11_lib:
                x11 = ctypes.CDLL(x11_lib, mode=ctypes.RTLD_GLOBAL)
                # Call XInitThreads - returns non-zero on success
                if hasattr(x11, 'XInitThreads'):
                    x11.XInitThreads()
        except Exception as e:
            # Silently fail if we can't load X11
            pass

# Call this before importing tkinter
_init_x11_threading()

from .config import AppConfig
from .core import WordReader
from .ui import WPMWindow


class WPMApp:
    """Main Words Per Minute application."""
    
    def __init__(self, config: Optional[AppConfig] = None) -> None:
        """Initialize the application.
        
        Args:
            config: Optional pre-configured AppConfig. If None, will prompt user.
        """
        self.config: Optional[AppConfig] = config
        self.reader: Optional[WordReader] = None
        self.window: Optional[WPMWindow] = None
        
    def initialize(self) -> None:
        """Initialize all application components.
        
        Raises:
            ValueError: If configuration or file reading fails
            FileNotFoundError: If paragraph file cannot be found
        """
        # Get configuration if not provided
        if self.config is None:
            try:
                # Check for Wayland and show info
                self._check_display_server()
                self.config = AppConfig.from_user_input()
            except (ValueError, KeyboardInterrupt) as e:
                print(f"\nConfiguration failed: {e}")
                sys.exit(1)
        
        # Initialize word reader
        try:
            self.reader = WordReader(self.config.paragraph_file)
        except (FileNotFoundError, ValueError) as e:
            print(f"\nError loading paragraph file: {e}")
            sys.exit(1)
        
        # Initialize window
        self.window = WPMWindow(self.config, self.reader)
        
    def run(self) -> None:
        """Run the application.
        
        This is the main entry point that sets up and starts the application.
        """
        if not self.window:
            raise RuntimeError("Application must be initialized before running")
        
        try:
            # Setup the window
            self.window.setup()
            
            # Show instructions
            self.window.show_instructions()
            
            # Start the word display
            self.window.start()
            
            # Run the main loop
            self.window.run()
            
        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\n\nUnexpected error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        finally:
            self._cleanup()
    
    def _check_display_server(self) -> None:
        """Check and inform about the display server being used."""
        wayland_display = os.environ.get('WAYLAND_DISPLAY')
        xdg_session_type = os.environ.get('XDG_SESSION_TYPE')
        
        if wayland_display or xdg_session_type == 'wayland':
            print("ℹ️  Detected Wayland display server")
            print("   Using Wayland-compatible fullscreen mode")
            print("   Note: Running tkinter through XWayland\n")
    
    def _cleanup(self) -> None:
        """Clean up application resources."""
        if self.window:
            self.window.cleanup()


def main() -> None:
    """Main entry point for the Words Per Minute application."""
    try:
        app = WPMApp()
        app.initialize()
        app.run()
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
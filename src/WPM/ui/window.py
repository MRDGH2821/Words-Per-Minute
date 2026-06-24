"""Modern GUI window for Words Per Minute application.

This module provides the main application window with fullscreen support
and keyboard controls.
"""

import tkinter as tk
from typing import Callable, Optional
import sys
import os
import platform
import threading

from ..config import AppConfig
from ..core import WordReader


class WPMWindow:
    """Main application window for displaying words."""
    
    def __init__(self, config: AppConfig, reader: WordReader) -> None:
        """Initialize the WPM window.
        
        Args:
            config: Application configuration
            reader: Word reader instance
        """
        self.config = config
        self.reader = reader
        self.root: Optional[tk.Tk] = None
        self.label: Optional[tk.Label] = None
        self.word_var: Optional[tk.StringVar] = None
        self._is_paused: bool = False
        self._after_id: Optional[str] = None
        self._is_wayland: bool = self._detect_wayland()
        self._fullscreen_state: bool = False
    
    def _detect_wayland(self) -> bool:
        """Detect if running on Wayland.
        
        Returns:
            True if running on Wayland, False otherwise
        """
        # Check common Wayland environment variables
        wayland_display = os.environ.get('WAYLAND_DISPLAY')
        xdg_session_type = os.environ.get('XDG_SESSION_TYPE')
        
        return (wayland_display is not None or 
                xdg_session_type == 'wayland')
    
    def setup(self) -> None:
        """Set up the main window and its components."""
        # Fix for XWayland threading issues
        if self._is_wayland:
            # Force single-threaded mode for XWayland
            try:
                os.environ['TK_SILENCE_DEPRECATION'] = '1'
            except:
                pass
        
        self.root = tk.Tk()
        self.root.title(self.config.window_title)
        
        # Set up key bindings first (before fullscreen for Wayland)
        self._setup_key_bindings()
        
        # Create the word display label
        self._setup_label()
        
        # Set fullscreen (must be done after widgets are created for Wayland)
        if self.config.fullscreen:
            self._set_fullscreen_wayland_safe(True)
        
    def _setup_key_bindings(self) -> None:
        """Set up keyboard shortcuts."""
        if not self.root:
            return
            
        # Toggle fullscreen
        self.root.bind("<F11>", self._toggle_fullscreen)
        
        # Exit fullscreen
        self.root.bind("<F1>", lambda e: self._set_fullscreen(False))
        
        # Close application
        self.root.bind("<Escape>", self._on_close)
        
        # Pause/Resume
        self.root.bind("<space>", self._toggle_pause)
        
        # Reset to beginning
        self.root.bind("<r>", self._reset)
        self.root.bind("<R>", self._reset)
        
    def _setup_label(self) -> None:
        """Create and configure the word display label."""
        if not self.root:
            return
            
        self.word_var = tk.StringVar()
        self.word_var.set("")
        
        self.label = tk.Label(
            self.root,
            textvariable=self.word_var,
            bg=self.config.background_color,
            fg=self.config.text_color,
            font=(self.config.font_family, self.config.font_size),
            anchor="center",
        )
        
        # Make label fill the entire window
        self.label.pack(fill=tk.BOTH, expand=True)
        
    def _toggle_fullscreen(self, event: Optional[tk.Event] = None) -> None:
        """Toggle fullscreen mode."""
        if not self.root:
            return
            
        self._set_fullscreen_wayland_safe(not self._fullscreen_state)
        
    def _set_fullscreen_wayland_safe(self, fullscreen: bool) -> None:
        """Set fullscreen state with Wayland compatibility.
        
        Args:
            fullscreen: True to enable fullscreen, False to disable
        """
        if not self.root:
            return
        
        try:
            if self._is_wayland:
                # Wayland-compatible fullscreen approach
                if fullscreen:
                    # Update widgets before changing state
                    self.root.update_idletasks()
                    
                    # Get screen dimensions first
                    screen_width = self.root.winfo_screenwidth()
                    screen_height = self.root.winfo_screenheight()
                    
                    # Set geometry to fullscreen
                    self.root.geometry(f"{screen_width}x{screen_height}+0+0")
                    
                    # Try to remove decorations (may not work on all Wayland compositors)
                    try:
                        self.root.overrideredirect(True)
                    except:
                        pass
                    
                    # Try to maximize
                    try:
                        self.root.state('zoomed')
                    except:
                        pass
                    
                    # Lift window to top
                    self.root.lift()
                    try:
                        self.root.attributes('-topmost', True)
                    except:
                        pass
                else:
                    # Restore window
                    try:
                        self.root.attributes('-topmost', False)
                    except:
                        pass
                    try:
                        self.root.overrideredirect(False)
                    except:
                        pass
                    try:
                        self.root.state('normal')
                    except:
                        pass
                    # Set a reasonable default size
                    self.root.geometry("800x600")
            else:
                # X11 standard fullscreen
                self.root.attributes("-fullscreen", fullscreen)
            
            self._fullscreen_state = fullscreen
            
        except tk.TclError as e:
            # Fallback if attributes don't work
            print(f"Warning: Fullscreen mode may not work properly: {e}")
            try:
                # Try alternative method
                if fullscreen:
                    self.root.state('zoomed')
                else:
                    self.root.state('normal')
                self._fullscreen_state = fullscreen
            except:
                print("Warning: Could not set fullscreen mode")
    
    def _set_fullscreen(self, fullscreen: bool) -> None:
        """Set fullscreen state (legacy method, redirects to Wayland-safe version).
        
        Args:
            fullscreen: True to enable fullscreen, False to disable
        """
        self._set_fullscreen_wayland_safe(fullscreen)
            
    def _toggle_pause(self, event: Optional[tk.Event] = None) -> None:
        """Toggle pause/resume state."""
        self._is_paused = not self._is_paused
        
        if not self._is_paused and self._after_id is None:
            # Resume if paused
            self._update_word()
            
    def _reset(self, event: Optional[tk.Event] = None) -> None:
        """Reset to the beginning of the text."""
        self.reader.reset()
        if self.word_var:
            self.word_var.set(self.reader.get_current_word())
            
    def _on_close(self, event: Optional[tk.Event] = None) -> None:
        """Handle window close event."""
        if self.root:
            self.root.quit()
            self.root.destroy()
        sys.exit(0)
        
    def _update_word(self) -> None:
        """Update the displayed word and schedule the next update."""
        if not self.root or not self.word_var or self._is_paused:
            return
            
        # Get and display the next word
        word = self.reader.next_word()
        self.word_var.set(word)
        
        # Schedule next update
        self._after_id = self.root.after(
            self.config.milliseconds_per_word,
            self._update_word
        )
        
    def show_instructions(self) -> None:
        """Show instructions to the user before starting."""
        if not self.root:
            return
            
        print("\n" + "=" * 60)
        print("INSTRUCTIONS")
        print("=" * 60)
        print("  <Escape>  : Close the program")
        print("  <F1>      : Exit fullscreen mode")
        print("  <F11>     : Toggle fullscreen/windowed mode")
        print("  <Space>   : Pause/Resume")
        print("  <R>       : Reset to beginning")
        print("=" * 60)
        print(f"\nTotal words: {self.reader.total_words}")
        print(f"Speed: {self.config.words_per_minute:.1f} WPM ({self.config.words_per_second} WPS)")
        print(f"Font size: {self.config.font_size}")
        print("\n**Note: Keys work after clicking on the window**\n")
        
        input("Press Enter to start...")
        
    def start(self) -> None:
        """Start the word display loop."""
        if not self.root:
            raise RuntimeError("Window must be set up before starting")
            
        # Show the first word
        if self.word_var:
            self.word_var.set(self.reader.get_current_word())
        
        # Start the update loop
        self._update_word()
        
    def run(self) -> None:
        """Run the main event loop."""
        if not self.root:
            raise RuntimeError("Window must be set up before running")
        
        # Force update before mainloop to avoid XWayland threading issues
        try:
            self.root.update_idletasks()
        except:
            pass
            
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self._on_close()
            
    def cleanup(self) -> None:
        """Clean up resources."""
        if self._after_id and self.root:
            self.root.after_cancel(self._after_id)
            
        if self.root:
            try:
                self.root.destroy()
            except tk.TclError:
                pass  # Window already destroyed
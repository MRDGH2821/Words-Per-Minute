"""Configuration settings for Words Per Minute application.

This module handles user configuration with validation and default values.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class AppConfig:
    """Application configuration with validation."""
    
    font_size: int = 100
    words_per_second: float = 2.0  # Default: 120 WPM
    paragraph_file: Path = field(default_factory=lambda: Path("para.txt"))
    fullscreen: bool = True
    background_color: str = "Black"
    text_color: str = "White"
    font_family: str = "Times"
    
    # Display settings
    window_title: str = "Words Per Minute"
    version: str = "1.0.1"
    
    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        self._validate()
    
    def _validate(self) -> None:
        """Validate configuration values."""
        if self.font_size < 10 or self.font_size > 500:
            raise ValueError(f"Font size must be between 10 and 500, got {self.font_size}")
        
        if self.words_per_second <= 0:
            raise ValueError(f"Words per second must be positive, got {self.words_per_second}")
        
        if self.words_per_second > 20:
            raise ValueError(f"Words per second too high (max 20), got {self.words_per_second}")
    
    @property
    def words_per_minute(self) -> float:
        """Convert WPS to WPM for display."""
        return self.words_per_second * 60
    
    @property
    def milliseconds_per_word(self) -> int:
        """Calculate milliseconds between word displays."""
        return int(1000 / self.words_per_second)
    
    @classmethod
    def from_user_input(cls) -> "AppConfig":
        """Create configuration from user input with proper error handling."""
        print(f"Words Per Minute! v{cls.version}\n")
        print("Use <Escape>, <F11> or <F1> to manipulate the window's fullscreen properties!\n")
        print("Configuration Menu:\n")
        
        font_size = cls._get_font_size()
        words_per_second = cls._get_words_per_second()
        paragraph_file = cls._get_paragraph_file()
        
        return cls(
            font_size=font_size,
            words_per_second=words_per_second,
            paragraph_file=paragraph_file,
        )
    
    @staticmethod
    def _get_font_size() -> int:
        """Prompt user for font size with validation."""
        while True:
            try:
                user_input = input("Enter Font size (100 default, press Enter to use default): ").strip()
                if not user_input:
                    return 100
                
                font_size = int(user_input)
                if 10 <= font_size <= 500:
                    return font_size
                print("Font size must be between 10 and 500. Please try again.")
            except ValueError:
                print("Invalid input. Using default font size: 100")
                return 100
    
    @staticmethod
    def _get_words_per_second() -> float:
        """Prompt user for words per second with validation."""
        print("\nYou might be familiar with Words per Minute (WPM).")
        print("This program uses Words per Second (WPS) convention.")
        print("Please divide WPM by 60 and enter the value here.")
        print("Default: 2 WPS (120 WPM)\n")
        
        while True:
            try:
                user_input = input(
                    "Enter Words per Second (higher = faster, press Enter for default): "
                ).strip()
                
                if not user_input:
                    return 2.0
                
                wps = float(user_input)
                if 0.1 <= wps <= 20:
                    return wps
                print("Words per second must be between 0.1 and 20. Please try again.")
            except ValueError:
                print("Invalid input. Using default: 2 WPS (120 WPM)")
                return 2.0
    
    @staticmethod
    def _get_paragraph_file() -> Path:
        """Get or create paragraph file from user input."""
        para_path = Path("para.txt")
        
        try:
            if para_path.exists():
                choice = input(
                    "\n0. Use existing paragraph\n"
                    "1. Create new paragraph\n"
                    "Enter choice (0 default, press Enter to use existing): "
                ).strip()
                
                if choice == "1":
                    raise FileNotFoundError("User chose to create new paragraph")
                
                # Validate existing file has content
                if para_path.stat().st_size == 0:
                    print("Existing paragraph file is empty. Please create a new one.")
                    raise FileNotFoundError("Empty file")
                
                return para_path
            else:
                raise FileNotFoundError("Paragraph file does not exist")
                
        except (FileNotFoundError, ValueError):
            print("\nEnter/Paste your content.")
            print("To save: Press Ctrl+D (Linux/Mac) or Ctrl+Z then Enter (Windows)\n")
            
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            
            content = "\n".join(lines)
            if not content.strip():
                raise ValueError("Paragraph cannot be empty")
            
            para_path.write_text(content, encoding="utf-8")
            print(f"\nParagraph saved to {para_path}")
            
            return para_path
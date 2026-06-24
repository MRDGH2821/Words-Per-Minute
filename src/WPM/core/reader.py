"""Core word reader logic for Words Per Minute application.

This module handles the reading and processing of text content.
"""

from pathlib import Path
from typing import List


class WordReader:
    """Manages reading and processing text content."""
    
    def __init__(self, file_path: Path) -> None:
        """Initialize the word reader.
        
        Args:
            file_path: Path to the text file to read
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is empty
        """
        self.file_path = file_path
        self._words: List[str] = []
        self._current_index: int = 0
        self._load_words()
    
    def _load_words(self) -> None:
        """Load and parse words from the file.
        
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is empty or contains no valid words
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        content = self.file_path.read_text(encoding="utf-8")
        
        if not content.strip():
            raise ValueError(f"File is empty: {self.file_path}")
        
        # Split on whitespace and filter empty strings
        self._words = [word for word in content.split() if word.strip()]
        
        if not self._words:
            raise ValueError(f"No valid words found in: {self.file_path}")
    
    @property
    def words(self) -> List[str]:
        """Get the list of words."""
        return self._words.copy()
    
    @property
    def total_words(self) -> int:
        """Get the total number of words."""
        return len(self._words)
    
    @property
    def current_index(self) -> int:
        """Get the current word index."""
        return self._current_index
    
    def get_current_word(self) -> str:
        """Get the current word.
        
        Returns:
            The current word at the current index
        """
        if not self._words:
            return ""
        return self._words[self._current_index]
    
    def next_word(self) -> str:
        """Move to and return the next word.
        
        Returns:
            The next word, or loops back to the first word if at the end
        """
        self._current_index = (self._current_index + 1) % len(self._words)
        return self.get_current_word()
    
    def reset(self) -> None:
        """Reset the word index to the beginning."""
        self._current_index = 0
    
    def has_more_words(self) -> bool:
        """Check if there are more words to display.
        
        Returns:
            True if not at the end, False if at the last word
        """
        return self._current_index < len(self._words) - 1
    
    def get_progress(self) -> tuple[int, int]:
        """Get the current reading progress.
        
        Returns:
            Tuple of (current_position, total_words)
        """
        return (self._current_index + 1, len(self._words))
    
    def get_progress_percentage(self) -> float:
        """Get the reading progress as a percentage.
        
        Returns:
            Progress percentage (0-100)
        """
        if not self._words:
            return 0.0
        return (self._current_index / len(self._words)) * 100
    
    def reload(self) -> None:
        """Reload words from the file and reset the index."""
        self._current_index = 0
        self._load_words()
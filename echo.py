#!/usr/bin/env python3
"""
Echo module for demonstrating text processing capabilities.
"""

import sys
from typing import Optional, List, Union


class Echo:
    """Echo class for text processing and output."""
    
    def __init__(self, prefix: str = "", suffix: str = ""):
        """Initialize Echo with optional prefix and suffix.
        
        Args:
            prefix: String to prepend to echoed text
            suffix: String to append to echoed text
        """
        self.prefix = prefix
        self.suffix = suffix
        self._history: List[str] = []
    
    def echo(self, text: Union[str, List[str]], 
             store_history: bool = True) -> str:
        """Echo the given text with optional prefix/suffix.
        
        Args:
            text: Text to echo (string or list of strings)
            store_history: Whether to store in history
            
        Returns:
            Processed echo string
        """
        if isinstance(text, list):
            text = " ".join(str(item) for item in text)
        
        result = f"{self.prefix}{text}{self.suffix}"
        
        if store_history:
            self._history.append(result)
        
        return result
    
    def echo_upper(self, text: str) -> str:
        """Echo text in uppercase.
        
        Args:
            text: Text to echo in uppercase
            
        Returns:
            Uppercase echo string
        """
        return self.echo(text.upper())
    
    def echo_lower(self, text: str) -> str:
        """Echo text in lowercase.
        
        Args:
            text: Text to echo in lowercase
            
        Returns:
            Lowercase echo string
        """
        return self.echo(text.lower())
    
    def echo_reverse(self, text: str) -> str:
        """Echo text in reverse.
        
        Args:
            text: Text to reverse and echo
            
        Returns:
            Reversed echo string
        """
        return self.echo(text[::-1])
    
    def echo_repeat(self, text: str, times: int = 1, 
                    separator: str = " ") -> str:
        """Echo text repeated multiple times.
        
        Args:
            text: Text to repeat
            times: Number of repetitions
            separator: Separator between repetitions
            
        Returns:
            Repeated echo string
        """
        if times < 0:
            raise ValueError("Repetition count must be non-negative")
        
        repeated = separator.join([text] * times)
        return self.echo(repeated)
    
    def get_history(self) -> List[str]:
        """Get the history of echoed strings.
        
        Returns:
            List of previously echoed strings
        """
        return self._history.copy()
    
    def clear_history(self) -> None:
        """Clear the echo history."""
        self._history.clear()
    
    def echo_file(self, filepath: str) -> Optional[str]:
        """Echo contents of a file.
        
        Args:
            filepath: Path to file to echo
            
        Returns:
            File contents as echoed string, or None if error
        """
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            return self.echo(content)
        except (FileNotFoundError, IOError) as e:
            return None


def main(args: List[str] = None) -> int:
    """Main CLI entry point for echo.
    
    Args:
        args: Command line arguments
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    if args is None:
        args = sys.argv[1:]
    
    if not args:
        print("Usage: echo.py <text>")
        return 1
    
    echo = Echo()
    result = echo.echo(" ".join(args))
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
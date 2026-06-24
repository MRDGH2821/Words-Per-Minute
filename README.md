# Words Per Minute!

A modern, fullscreen speed-reading trainer that displays text word by word at customizable speeds.

## Features

- 🚀 **Customizable Speed**: Set your reading pace in Words Per Second (WPS) or Words Per Minute (WPM)
- 🎨 **Fullscreen Display**: Distraction-free reading experience
- ⌨️ **Keyboard Controls**: 
  - `Escape` - Close the application
  - `F1` - Exit fullscreen mode
  - `F11` - Toggle fullscreen/windowed mode
  - `Space` - Pause/Resume reading
  - `R` - Reset to beginning
- 📝 **Custom Text**: Use your own paragraphs for training
- 🎯 **Clean, Modern Codebase**: Built with Python 3.12+ using modern best practices

## Quick Start

### Installation

```bash
# Using uv (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

### Usage

```bash
# Run the application
wpm

# Or
wpm-gui
```

### First Run

1. The application will prompt you for:
   - Font size (default: 100)
   - Reading speed in Words Per Second (default: 2.0 WPS = 120 WPM)
   - Your paragraph text

2. Press Enter to start displaying words

3. Use keyboard shortcuts to control the display

## Advanced Usage

### Programmatic Usage

```python
from WPM import WPMApp, AppConfig

# Use with custom configuration
config = AppConfig(
    font_size=120,
    words_per_second=2.5,  # 150 WPM
    background_color="Navy",
    text_color="Yellow"
)

app = WPMApp(config=config)
app.initialize()
app.run()
```

See `example_usage.py` for more examples.

## What's New (Modernization)

This codebase has been completely modernized with:

- ✅ **Type Safety**: Full type hints throughout
- ✅ **Modular Architecture**: Clean separation of concerns (config, core, UI)
- ✅ **Modern Python**: Dataclasses, pathlib, proper error handling
- ✅ **Enhanced Features**: Pause/resume, reset, progress tracking
- ✅ **Better UX**: Input validation, helpful error messages
- ✅ **Documentation**: Comprehensive docstrings and type hints
- ✅ **No External Dependencies**: Uses only Python standard library (tkinter)

See [MODERNIZATION.md](MODERNIZATION.md) for detailed information about the improvements.

## Project Structure

```
src/WPM/
├── __init__.py          # Package interface
├── app.py               # Main application
├── WPM.py               # Legacy compatibility wrapper
├── config/
│   └── settings.py      # Configuration management
├── core/
│   └── reader.py        # Word reading logic
└── ui/
    └── window.py        # GUI components
```

## Requirements

- Python 3.12 or higher
- tkinter (usually included with Python)

## Demo

Check out how it works [here](https://youtu.be/LsUXx_7NaLo)

Download releases [here](https://github.com/MRDGH2821/Words-Per-Minute-/releases)

## Development

### Building

```bash
# Build distribution packages
uv build
```

### Contributing

Contributions are welcome! The modernized codebase makes it easy to:
- Add new features
- Write tests
- Extend functionality
- Improve documentation

## License

See [LICENCE.txt](LICENCE.txt) for details.

## Acknowledgments

Original concept and implementation with modern improvements.

### References

- [How to Create Full Screen Window in Tkinter](https://www.delftstack.com/howto/python-tkinter/how-to-create-full-screen-window-in-tkinter/)
- [Python Tkinter refresh canvas](https://stackoverflow.com/questions/21357178/python-tkinter-refresh-canvas)
- [Python Canvas.create_text Examples](https://python.hotexamples.com/examples/tkinter/Canvas/create_text/python-canvas-create_text-method-examples.html)
- [How to get multiline input from user](https://stackoverflow.com/questions/30239092/how-to-get-multiline-input-from-user)
- [Python exit commands](https://www.geeksforgeeks.org/python-exit-commands-quit-exit-sys-exit-and-os-_exit/)
- [Tkinter - Inserting text into canvas windows](https://stackoverflow.com/questions/14423959/tkinter-inserting-text-into-canvas-windows)
- [Getting screen's height and width using Tkinter | Python](https://www.geeksforgeeks.org/getting-screens-height-and-width-using-tkinter-python/)
- [Canvas Text update - Python3 Tkinter](https://stackoverflow.com/questions/52792254/canvas-text-update-python3-tkinter)
- [Add a text to canvas in Tkinter (Python)](https://youtu.be/jxUjqr4dMpc)
- [How to Update text in Tkinter Label/Canvas widget using for loop?](https://stackoverflow.com/questions/63270650/how-to-update-text-in-tkinter-label-canvas-widget-using-for-loop)

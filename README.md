# Console File Editor (CFE)

CFE is a Python-based text editor that runs in the console using the curses library. It provides a simple yet powerful interface for editing text files directly in your terminal.

## Features

- File loading and saving
- Cursor movement
- Text insertion and deletion
- Undo/Redo functionality
- Syntax highlighting for Python
- Line numbering
- Search functionality
- Auto-completion for Python keywords

## Project Structure

The project consists of the following main files:

- `main.py`: Entry point of the application
- `cfe_core.py`: Contains the main `CFEditor` class
- `config.py`: Holds configuration settings
- `utils.py`: Utility functions and classes

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Clone this repository:
   ```
   git clone https://github.com/mk-samoilov/Console-File-Editor.git
   cd Console-File-Editor
   ```
   - And if you usage windows: `pip install -r windows-requiments.txt`
3. No additional dependencies are required as CFE uses Python's built-in libraries.

## Usage

To run the Console File Editor, use the following command:

```
python main.py <filename>
```

If you provide a filename as an argument, CFE will open that file directly. If the file doesn't exist, it will be created. If no filename is provided, you'll see a menu where you can choose to open a file or exit the program.

### Key Bindings

- **Ctrl+S**: Save file
- **Ctrl+Q**: Quit
- **Ctrl+F**: Find (search)
- **Ctrl+L**: Toggle line numbers
- **Ctrl+Z**: Undo
- **Ctrl+Y**: Redo
- **Tab**: Auto-complete
- **Arrow keys**: Move cursor
- **Enter**: Insert new line
- **Backspace**: Delete character before cursor
- **Delete**: Delete character at cursor

## Configuration

The `CFEConfiguration` class in `config.py` defines key bindings and color settings for syntax highlighting. You can modify these settings to customize the editor's behavior and appearance.

## Potential Improvements

1. Error handling: Implement more robust error handling, especially for file operations.
2. Testing: Add unit tests for core functionality.
3. User-defined configuration: Allow users to create and load custom configuration files.
4. Extended language support: Add syntax highlighting for more programming languages.
5. Performance optimization: Improve efficiency for handling larger files.

## Contributing

Contributions to the Console File Editor are welcome! Please feel free to submit a Pull Request.
- `me@mk-samoilov.ru` (can be written in any language)

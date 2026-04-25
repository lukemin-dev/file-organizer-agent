# File Organizer Agent

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

A Python-based file organization tool that automatically categorizes and organizes files in a directory based on their file extensions. This tool helps maintain a clean and structured file system by grouping similar files into appropriate category folders.

This project was developed using an AI agent-assisted workflow, including planning, implementation, review, testing, and documentation.

## Features

- **Automatic File Categorization**: Organizes files into predefined categories based on file extensions
- **Dry-Run Mode**: Preview organization changes before applying them
- **Duplicate Handling**: Automatically handles duplicate filenames by appending numbers
- **Comprehensive Logging**: Logs all operations to both file and console
- **Command Line Interface**: Simple and intuitive CLI with flexible options
- **Extensible Categories**: Easy to add new file categories and extensions
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Supported Categories

- **PDF**: `.pdf`
- **Slides**: `.pptx`, `.ppt`, `.odp`
- **Docs**: `.docx`, `.doc`, `.odt`, `.txt`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`
- **Installers**: `.exe`, `.msi`, `.dmg`, `.pkg`
- **Archives**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`
- **Code**: `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`, `.c`, `.h`
- **Data**: `.csv`, `.xlsx`, `.xls`, `.json`, `.xml`
- **Others**: All other file extensions

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Install from Source

1. Clone or download the repository:
   ```bash
   git clone <repository-url>
   cd file-organizer-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

The program has minimal dependencies and should work out of the box on most Python installations.

## Usage

### Basic Usage

Organize files in your Downloads folder (dry-run mode):
```bash
python -m src.main
```

Organize files in a specific directory:
```bash
python -m src.main --target /path/to/your/directory
```

Apply the organization (move files):
```bash
python -m src.main --target /path/to/your/directory --apply
```

**Note**: Hidden files (starting with `.`) are automatically excluded from organization to prevent accidental movement of system files like `.DS_Store`, `.localized`, etc.

### Command Line Options

- `--target PATH`: Specify the target directory to organize (default: ~/Downloads)
- `--apply`: Apply the organization by moving files (default: dry-run mode only)

### Examples

#### Example 1: Preview organization of Downloads folder
```bash
python -m src.main
```
Output:
```
Planned to organize 15 files:
  PDF: 3 files
  Images: 5 files
  Docs: 2 files
  Archives: 2 files
  Others: 3 files
Would move document.pdf to PDF/document.pdf
Would move photo.jpg to Images/photo.jpg
...
```

#### Example 2: Organize a specific folder
```bash
python -m src.main --target ./messy_folder --apply
```
Output:
```
Planned to organize 8 files:
  Code: 3 files
  Data: 2 files
  Others: 3 files
Moved script.py to Code/script.py
Moved data.csv to Data/data.csv
...
```

#### Example 3: Handle duplicate filenames
If you have multiple files with the same name, the organizer automatically creates unique names:
```
original.txt -> Docs/original.txt
original.txt -> Docs/original_1.txt
original.txt -> Docs/original_2.txt
```

## Configuration

### Default Target Directory

By default, the organizer targets your system's Downloads folder:
- **macOS/Linux**: `~/Downloads`
- **Windows**: `C:\Users\<username>\Downloads`

You can change this default by modifying `src/config.py`:
```python
DEFAULT_TARGET = Path.home() / "Downloads"  # Change this path
```

### Adding New Categories

To add new file categories, edit `src/config.py`:
```python
CATEGORIES = {
    "PDF": ["pdf"],
    "Slides": ["pptx", "ppt", "odp"],
    "YourNewCategory": ["ext1", "ext2", "ext3"],  # Add your category
    "Others": []
}
```

## Logging

The organizer creates detailed logs of all operations:

- **Log File**: `logs/organizer.log`
- **Console Output**: Real-time progress and results
- **Log Format**: Timestamp, level, and message

Example log entry:
```
2024-01-15 10:30:15 - INFO - Starting file organizer on /Users/user/Downloads, apply=False
2024-01-15 10:30:15 - INFO - DRY RUN: Would move document.pdf to PDF/document.pdf
2024-01-15 10:30:16 - INFO - File organization completed.
```

## Requirements

- **Python**: 3.7+
- **Dependencies**: None (uses only Python standard library)
- **Operating System**: Windows, macOS, Linux

### Development Dependencies

For testing and development:
- pytest
- pytest-cov

## Testing

The project includes comprehensive unit tests and integration tests.

### Running Tests

Install test dependencies:
```bash
pip install -r requirements.txt
```

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

Run specific test categories:
```bash
pytest -m "not slow"  # Skip slow tests
pytest tests/test_organizer.py  # Run specific test file
```

### Manual Testing

For manual testing procedures, see `MANUAL_TESTING.md`.

## Project Structure

```
file-organizer-agent/
├── src/
│   ├── main.py          # CLI entry point
│   ├── organizer.py     # Core organization logic
│   ├── config.py        # Configuration and categories
│   └── utils.py         # Utility functions
├── tests/
│   ├── test_*.py        # Unit tests
│   └── conftest.py      # Test fixtures
├── logs/                # Log files (created at runtime)
├── sample_downloads/    # Sample files for testing
├── requirements.txt     # Python dependencies
├── pytest.ini          # Pytest configuration
├── MANUAL_TESTING.md   # Manual testing guide
└── README.md           # This file
```

## Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Install development dependencies: `pip install -r requirements.txt`
4. Run tests: `pytest`
5. Make your changes
6. Add tests for new functionality
7. Ensure all tests pass
8. Update documentation if needed
9. Commit your changes: `git commit -m "Add your feature"`
10. Push to your fork: `git push origin feature/your-feature-name`
11. Create a Pull Request

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write descriptive commit messages
- Add docstrings to all public functions and classes

### Testing

- Write unit tests for all new functionality
- Maintain test coverage above 80%
- Test edge cases and error conditions
- Run the full test suite before submitting PRs

### Reporting Issues

When reporting bugs or requesting features:

1. Check existing issues first
2. Use a clear, descriptive title
3. Provide steps to reproduce the issue
4. Include your environment (OS, Python version)
5. Attach relevant log files if available

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### Version 1.0.0
- Initial release
- Basic file organization functionality
- Dry-run mode
- Command line interface
- Comprehensive test suite
- Logging support

## Support

If you encounter any issues or have questions:

1. Check the troubleshooting section in `MANUAL_TESTING.md`
2. Review the logs in `logs/organizer.log`
3. Search existing issues on GitHub
4. Create a new issue with detailed information

## Roadmap

Future enhancements may include:
- GUI interface
- Custom category definitions via config file
- Undo functionality
- Integration with file managers
- Cloud storage support
- Advanced filtering options</content>
<parameter name="filePath">/Users/gyuminlee/Desktop/file-organizer-agent/README.md
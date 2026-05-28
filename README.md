# File Organizer Agent

[![CI](https://github.com/lukemin-dev/file-organizer-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/lukemin-dev/file-organizer-agent/actions/workflows/ci.yml)

[English](README.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

A Python CLI tool that categorizes files by extension and moves them into organized folders. It defaults to dry-run mode, so you can preview the planned changes before moving anything.

## Features

- Automatic file categorization by extension
- Dry-run mode by default
- Duplicate filename handling with numbered suffixes
- Hidden-file exclusion for files like `.DS_Store`
- File and console logging
- Cross-platform Python implementation
- Unit and integration tests with pytest

## Supported Categories

| Category | Extensions |
|---|---|
| PDF | `.pdf` |
| Slides | `.pptx`, `.ppt`, `.odp` |
| Docs | `.docx`, `.doc`, `.odt`, `.txt` |
| Images | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff` |
| Installers | `.exe`, `.msi`, `.dmg`, `.pkg` |
| Archives | `.zip`, `.rar`, `.7z`, `.tar`, `.gz` |
| Code | `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`, `.c`, `.h` |
| Data | `.csv`, `.xlsx`, `.xls`, `.json`, `.xml` |
| Others | Any unknown extension |

## Installation

```bash
git clone https://github.com/lukemin-dev/file-organizer-agent.git
cd file-organizer-agent
pip install -r requirements.txt
```

## Usage

Preview changes for the default Downloads folder:

```bash
python -m src.main
```

Preview a specific folder:

```bash
python -m src.main --target /path/to/your/directory
```

Apply the move operation:

```bash
python -m src.main --target /path/to/your/directory --apply
```

Example output:

```text
Planned to organize 8 files:
  Code: 3 files
  Data: 2 files
  Others: 3 files
Would move script.py to Code/script.py
```

## Logging

Logs are written to `logs/organizer.log`. The log directory is created automatically when the CLI starts.

## Testing

```bash
pytest
pytest --cov=src --cov-report=html
```

GitHub Actions runs `pytest` on `main` pushes and pull requests.

## Project Structure

```text
src/main.py        CLI entry point
src/organizer.py   Core organization logic
src/config.py      Categories and defaults
src/utils.py       Utility functions
tests/             Unit and integration tests
```

## Roadmap

- GUI interface
- Custom category definitions through a config file
- Undo functionality
- Advanced filtering options
- Cloud storage support

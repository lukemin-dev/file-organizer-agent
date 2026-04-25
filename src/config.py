from pathlib import Path

# Default target directory
DEFAULT_TARGET = Path.home() / "Downloads"

# File categories with their extensions
CATEGORIES = {
    "PDF": ["pdf"],
    "Slides": ["pptx", "ppt", "odp"],
    "Docs": ["docx", "doc", "odt", "txt"],
    "Images": ["jpg", "jpeg", "png", "gif", "bmp", "tiff"],
    "Installers": ["exe", "msi", "dmg", "pkg"],
    "Archives": ["zip", "rar", "7z", "tar", "gz"],
    "Code": ["py", "js", "html", "css", "java", "cpp", "c", "h"],
    "Data": ["csv", "xlsx", "xls", "json", "xml"],
    "Others": []  # Catch-all for unmatched extensions
}
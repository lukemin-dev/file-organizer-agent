from pathlib import Path
from src.config import CATEGORIES

def get_category(extension: str) -> str:
    """Get the category name for a given file extension."""
    extension = extension.lower().lstrip('.')
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"

def get_unique_name(target_dir: Path, filename: str) -> str:
    """Generate a unique filename by appending _1, _2, etc. if needed."""
    # For hidden files (starting with .), don't treat the first . as extension separator
    if filename.startswith('.') and filename.count('.') == 1:
        # Hidden file with no extension
        stem = filename
        suffix = ""
    elif '.' in filename:
        stem, suffix = filename.rsplit('.', 1)
        suffix = '.' + suffix
    else:
        stem = filename
        suffix = ""
    
    # Get existing filenames (case sensitive)
    if not target_dir.exists():
        return filename
    
    existing_names = {p.name for p in target_dir.iterdir() if p.is_file()}
    
    counter = 1
    unique_name = filename
    while unique_name in existing_names:
        unique_name = f"{stem}_{counter}{suffix}"
        counter += 1
    return unique_name
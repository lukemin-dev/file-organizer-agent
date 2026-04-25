import pytest
import tempfile
import shutil
from pathlib import Path

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)

@pytest.fixture
def sample_files(temp_dir):
    """Create sample files in temp directory."""
    # Create files with different extensions
    files = [
        ("document.pdf", "PDF content"),
        ("presentation.pptx", "Slides content"),
        ("text.docx", "Docs content"),
        ("image.jpg", "Image content"),
        ("installer.exe", "Installer content"),
        ("archive.zip", "Archive content"),
        ("script.py", "Code content"),
        ("data.csv", "Data content"),
        ("unknown.xyz", "Unknown content"),
        ("no_extension", "No extension content"),
    ]
    
    for filename, content in files:
        file_path = temp_dir / filename
        file_path.write_text(content)
    
    return temp_dir
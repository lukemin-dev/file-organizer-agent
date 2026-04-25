import pytest
from pathlib import Path
from src.utils import get_category, get_unique_name

class TestGetCategory:
    def test_pdf_extension(self):
        """Test PDF extension categorization."""
        assert get_category(".pdf") == "PDF"
        assert get_category("pdf") == "PDF"
        assert get_category(".PDF") == "PDF"
    
    def test_slides_extensions(self):
        """Test Slides extensions."""
        for ext in [".pptx", ".ppt", ".odp"]:
            assert get_category(ext) == "Slides"
    
    def test_docs_extensions(self):
        """Test Docs extensions."""
        for ext in [".docx", ".doc", ".odt", ".txt"]:
            assert get_category(ext) == "Docs"
    
    def test_images_extensions(self):
        """Test Images extensions."""
        for ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]:
            assert get_category(ext) == "Images"
    
    def test_installers_extensions(self):
        """Test Installers extensions."""
        for ext in [".exe", ".msi", ".dmg", ".pkg"]:
            assert get_category(ext) == "Installers"
    
    def test_archives_extensions(self):
        """Test Archives extensions."""
        for ext in [".zip", ".rar", ".7z", ".tar", ".gz"]:
            assert get_category(ext) == "Archives"
    
    def test_code_extensions(self):
        """Test Code extensions."""
        for ext in [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h"]:
            assert get_category(ext) == "Code"
    
    def test_data_extensions(self):
        """Test Data extensions."""
        for ext in [".csv", ".xlsx", ".xls", ".json", ".xml"]:
            assert get_category(ext) == "Data"
    
    def test_unknown_extension(self):
        """Test unknown extension goes to Others."""
        assert get_category(".xyz") == "Others"
        assert get_category("xyz") == "Others"
    
    def test_no_extension(self):
        """Test files with no extension go to Others."""
        assert get_category("") == "Others"
    
    def test_empty_string(self):
        """Test empty string."""
        assert get_category("") == "Others"

class TestGetUniqueName:
    def test_unique_name_when_no_conflict(self, temp_dir):
        """Test unique name when no file exists."""
        filename = "test.txt"
        result = get_unique_name(temp_dir, filename)
        assert result == "test.txt"
    
    def test_unique_name_with_conflict(self, temp_dir):
        """Test unique name when file already exists."""
        # Create existing file
        existing_file = temp_dir / "test.txt"
        existing_file.write_text("content")
        
        result = get_unique_name(temp_dir, "test.txt")
        assert result == "test_1.txt"
    
    def test_unique_name_multiple_conflicts(self, temp_dir):
        """Test unique name with multiple existing files."""
        # Create existing files
        (temp_dir / "test.txt").write_text("content")
        (temp_dir / "test_1.txt").write_text("content")
        (temp_dir / "test_2.txt").write_text("content")
        
        result = get_unique_name(temp_dir, "test.txt")
        assert result == "test_3.txt"
    
    def test_unique_name_no_extension(self, temp_dir):
        """Test unique name for files without extension."""
        # Create existing file
        (temp_dir / "test").write_text("content")
        
        result = get_unique_name(temp_dir, "test")
        assert result == "test_1"
    
    def test_unique_name_hidden_file_with_extension(self, temp_dir):
        """Test unique name for hidden files with extensions."""
        # Create existing file
        (temp_dir / ".hidden.txt").write_text("content")
        
        result = get_unique_name(temp_dir, ".hidden.txt")
        assert result == ".hidden_1.txt"
    
    def test_unique_name_case_sensitivity(self, temp_dir):
        """Test that unique name handles case sensitivity."""
        # Create existing file
        (temp_dir / "Test.txt").write_text("content")
        
        result = get_unique_name(temp_dir, "test.txt")
        # On case-sensitive file systems, these are different files
        assert result == "test.txt"
    
    def test_unique_name_with_numbers(self, temp_dir):
        """Test unique name when filename already has numbers."""
        # Create existing file
        (temp_dir / "file2.txt").write_text("content")
        
        result = get_unique_name(temp_dir, "file2.txt")
        assert result == "file2_1.txt"
    
    def test_unique_name_complex_filename(self, temp_dir):
        """Test unique name with complex filename."""
        filename = "complex-file_name.with.dots.txt"
        (temp_dir / filename).write_text("content")
        
        result = get_unique_name(temp_dir, filename)
        assert result == "complex-file_name.with.dots_1.txt"
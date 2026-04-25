import pytest
from pathlib import Path
from src.config import DEFAULT_TARGET, CATEGORIES

class TestConfig:
    def test_default_target_is_path(self):
        """Test that DEFAULT_TARGET is a Path object."""
        assert isinstance(DEFAULT_TARGET, Path)
    
    def test_default_target_points_to_downloads(self):
        """Test that DEFAULT_TARGET points to Downloads directory."""
        expected = Path.home() / "Downloads"
        assert DEFAULT_TARGET == expected
    
    def test_categories_is_dict(self):
        """Test that CATEGORIES is a dictionary."""
        assert isinstance(CATEGORIES, dict)
    
    def test_categories_has_expected_keys(self):
        """Test that CATEGORIES has all expected category keys."""
        expected_keys = ["PDF", "Slides", "Docs", "Images", "Installers", "Archives", "Code", "Data", "Others"]
        assert set(CATEGORIES.keys()) == set(expected_keys)
    
    def test_categories_extensions_are_lists(self):
        """Test that all category values are lists."""
        for category, extensions in CATEGORIES.items():
            assert isinstance(extensions, list), f"Category {category} should have list of extensions"
    
    def test_pdf_category(self):
        """Test PDF category extensions."""
        assert CATEGORIES["PDF"] == ["pdf"]
    
    def test_slides_category(self):
        """Test Slides category extensions."""
        assert CATEGORIES["Slides"] == ["pptx", "ppt", "odp"]
    
    def test_docs_category(self):
        """Test Docs category extensions."""
        assert CATEGORIES["Docs"] == ["docx", "doc", "odt", "txt"]
    
    def test_images_category(self):
        """Test Images category extensions."""
        assert CATEGORIES["Images"] == ["jpg", "jpeg", "png", "gif", "bmp", "tiff"]
    
    def test_installers_category(self):
        """Test Installers category extensions."""
        assert CATEGORIES["Installers"] == ["exe", "msi", "dmg", "pkg"]
    
    def test_archives_category(self):
        """Test Archives category extensions."""
        assert CATEGORIES["Archives"] == ["zip", "rar", "7z", "tar", "gz"]
    
    def test_code_category(self):
        """Test Code category extensions."""
        assert CATEGORIES["Code"] == ["py", "js", "html", "css", "java", "cpp", "c", "h"]
    
    def test_data_category(self):
        """Test Data category extensions."""
        assert CATEGORIES["Data"] == ["csv", "xlsx", "xls", "json", "xml"]
    
    def test_others_category_is_empty(self):
        """Test that Others category is empty (catch-all)."""
        assert CATEGORIES["Others"] == []
import pytest
from pathlib import Path
from src.organizer import FileOrganizer

class TestIntegration:
    def test_full_organization_workflow_dry_run(self, sample_files):
        """Test full organization workflow in dry run mode."""
        organizer = FileOrganizer(sample_files, dry_run=True)
        
        # Scan and plan
        organizer.scan_and_plan()
        
        # Get summary
        summary = organizer.get_summary()
        assert "Planned to organize 10 files:" in summary
        
        # Execute (dry run)
        organizer.execute()
        
        # Verify files are still in original location
        for file_path in sample_files.iterdir():
            if file_path.is_file():
                assert file_path.exists()
        
        # Verify no category directories created
        category_dirs = [d for d in sample_files.iterdir() if d.is_dir()]
        assert len(category_dirs) == 0
    
    def test_full_organization_workflow_real(self, sample_files):
        """Test full organization workflow with real moves."""
        organizer = FileOrganizer(sample_files, dry_run=False)
        
        # Scan and plan
        organizer.scan_and_plan()
        
        # Get summary
        summary = organizer.get_summary()
        assert "Planned to organize 10 files:" in summary
        
        # Execute (real moves)
        organizer.execute()
        
        # Verify files moved to category directories
        moved_files = []
        for category_dir in sample_files.iterdir():
            if category_dir.is_dir():
                for file_path in category_dir.iterdir():
                    moved_files.append(file_path)
        
        assert len(moved_files) == 10
        
        # Verify original directory is empty of files
        original_files = [f for f in sample_files.iterdir() if f.is_file()]
        assert len(original_files) == 0
    
    def test_category_directories_created(self, sample_files):
        """Test that appropriate category directories are created."""
        organizer = FileOrganizer(sample_files, dry_run=False)
        organizer.scan_and_plan()
        organizer.execute()
        
        expected_categories = ["PDF", "Slides", "Docs", "Images", "Installers", "Archives", "Code", "Data", "Others"]
        created_dirs = [d.name for d in sample_files.iterdir() if d.is_dir()]
        
        # Should have created directories for categories that have files
        assert "PDF" in created_dirs
        assert "Slides" in created_dirs
        assert "Docs" in created_dirs
        assert "Images" in created_dirs
        assert "Installers" in created_dirs
        assert "Archives" in created_dirs
        assert "Code" in created_dirs
        assert "Data" in created_dirs
        assert "Others" in created_dirs
    
    def test_file_name_uniqueness(self, temp_dir):
        """Test that duplicate filenames are handled with unique names."""
        # Create a file in the temp dir
        file1 = temp_dir / "test.pdf"
        file1.write_text("content 1")
        
        # Create PDF category directory with existing file
        pdf_dir = temp_dir / "PDF"
        pdf_dir.mkdir()
        existing_pdf = pdf_dir / "test.pdf"
        existing_pdf.write_text("existing content")
        
        # Now organize - the file should get renamed to test_1.pdf
        organizer = FileOrganizer(temp_dir, dry_run=False)
        organizer.scan_and_plan()
        organizer.execute()
        
        # Check that the new file got renamed
        assert (pdf_dir / "test_1.pdf").exists()
        assert (pdf_dir / "test.pdf").exists()  # Original still there
    
    def test_mixed_file_types_organization(self, temp_dir):
        """Test organizing a directory with mixed file types."""
        # Create various files
        files_to_create = [
            ("report.pdf", "PDF content"),
            ("presentation.pptx", "Slides content"),
            ("readme.txt", "Text content"),
            ("photo.jpg", "Image content"),
            ("setup.exe", "Installer content"),
            ("backup.zip", "Archive content"),
            ("script.py", "Code content"),
            ("data.csv", "Data content"),
            ("unknown.xyz", "Unknown content"),
        ]
        
        for filename, content in files_to_create:
            (temp_dir / filename).write_text(content)
        
        organizer = FileOrganizer(temp_dir, dry_run=False)
        organizer.scan_and_plan()
        organizer.execute()
        
        # Verify organization
        categories_created = [d.name for d in temp_dir.iterdir() if d.is_dir()]
        assert len(categories_created) == 9  # All categories except possibly some
        
        # Count total files moved
        total_moved = 0
        for category_dir in temp_dir.iterdir():
            if category_dir.is_dir():
                total_moved += len(list(category_dir.iterdir()))
        
        assert total_moved == len(files_to_create)
    
    def test_integration_with_logging(self, tmp_path, caplog):
        """Test full integration with logging enabled."""
        import logging
        from src.main import setup_logging
        
        # Setup logging to a file outside temp_dir
        log_file = tmp_path / "test.log"
        setup_logging(log_file)
        
        # Create test files in a subdir
        test_dir = tmp_path / "test_files"
        test_dir.mkdir()
        (test_dir / "test.pdf").write_text("content")
        
        # Run organization
        organizer = FileOrganizer(test_dir, dry_run=False)
        organizer.scan_and_plan()
        organizer.execute()
        
        # Check log file was created and has content
        assert log_file.exists()
        log_content = log_file.read_text()
        assert "Moved" in log_content
    
    def test_integration_dry_run_vs_real_run(self, temp_dir):
        """Test that dry run doesn't move files but real run does."""
        # Create test files
        files = ["test.pdf", "script.py", "data.csv"]
        for filename in files:
            (temp_dir / filename).write_text("content")
        
        # Dry run
        dry_organizer = FileOrganizer(temp_dir, dry_run=True)
        dry_organizer.scan_and_plan()
        dry_organizer.execute()
        
        # Files should still be in place
        for filename in files:
            assert (temp_dir / filename).exists()
        
        # Real run
        real_organizer = FileOrganizer(temp_dir, dry_run=False)
        real_organizer.scan_and_plan()
        real_organizer.execute()
        
        # Files should be moved
        for filename in files:
            assert not (temp_dir / filename).exists()
        
        # Category directories should exist
        assert (temp_dir / "PDF").exists()
        assert (temp_dir / "Code").exists()
        assert (temp_dir / "Data").exists()
    
    def test_integration_with_main_module(self, temp_dir, capsys):
        """Test integration by calling main module functions."""
        from src.main import main
        import sys
        from unittest.mock import patch
        
        # Create test files
        (temp_dir / "test.pdf").write_text("content")
        
        # Mock command line args
        with patch('sys.argv', ['main.py', '--target', str(temp_dir), '--apply']):
            with patch('src.main.setup_logging'):  # Prevent log file creation
                main()
        
        # Check that file was moved
        assert not (temp_dir / "test.pdf").exists()
        assert (temp_dir / "PDF" / "test.pdf").exists()
        
        # Check output
        captured = capsys.readouterr()
        assert "Moved" in captured.out or "Planned" in captured.out
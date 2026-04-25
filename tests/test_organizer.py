import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.organizer import FileOrganizer

class TestFileOrganizer:
    def test_init(self, temp_dir):
        """Test FileOrganizer initialization."""
        organizer = FileOrganizer(temp_dir, dry_run=True)
        assert organizer.target_dir == temp_dir
        assert organizer.dry_run is True
        assert organizer.actions == []
    
    def test_scan_and_plan_nonexistent_directory(self, temp_dir):
        """Test scan_and_plan with nonexistent directory."""
        nonexistent = temp_dir / "nonexistent"
        organizer = FileOrganizer(nonexistent, dry_run=True)
        
        with patch('src.organizer.logger') as mock_logger:
            organizer.scan_and_plan()
            mock_logger.warning.assert_called_once()
            assert organizer.actions == []
    
    def test_scan_and_plan_ignores_hidden_files(self, temp_dir):
        """Test that scan_and_plan ignores hidden files."""
        # Create normal and hidden files
        (temp_dir / "normal.pdf").write_text("content")
        (temp_dir / ".hidden.pdf").write_text("content")
        (temp_dir / ".DS_Store").write_text("content")
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer.scan_and_plan()
        
        # Should only plan to move the normal file
        assert len(organizer.actions) == 1
        source, dest = organizer.actions[0]
        assert source.name == "normal.pdf"
    
    def test_scan_and_plan_with_files(self, sample_files):
        """Test scan_and_plan with sample files."""
        organizer = FileOrganizer(sample_files, dry_run=True)
        organizer.scan_and_plan()
        
        # Should have 10 actions (10 sample files)
        assert len(organizer.actions) == 10
        
        # Check that each action is a tuple of (source, destination)
        for source, dest in organizer.actions:
            assert isinstance(source, Path)
            assert isinstance(dest, Path)
            assert source.parent == sample_files
            assert dest.parent.parent == sample_files  # dest is in category subdir
    
    def test_plan_file_move_pdf(self, temp_dir):
        """Test _plan_file_move for PDF file."""
        pdf_file = temp_dir / "test.pdf"
        pdf_file.write_text("content")
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer._plan_file_move(pdf_file)
        
        assert len(organizer.actions) == 1
        source, dest = organizer.actions[0]
        assert source == pdf_file
        assert dest.parent.name == "PDF"
        assert dest.name == "test.pdf"
    
    def test_plan_file_move_unknown_extension(self, temp_dir):
        """Test _plan_file_move for unknown extension."""
        unknown_file = temp_dir / "test.xyz"
        unknown_file.write_text("content")
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer._plan_file_move(unknown_file)
        
        assert len(organizer.actions) == 1
        source, dest = organizer.actions[0]
        assert source == unknown_file
        assert dest.parent.name == "Others"
        assert dest.name == "test.xyz"
    
    def test_execute_dry_run(self, sample_files):
        """Test execute in dry run mode."""
        organizer = FileOrganizer(sample_files, dry_run=True)
        organizer.scan_and_plan()
        
        with patch('src.organizer.logger') as mock_logger:
            with patch('builtins.print') as mock_print:
                organizer.execute()
                
                # Should log dry run messages
                assert mock_logger.info.call_count == len(organizer.actions)
                # Should print messages
                assert mock_print.call_count == len(organizer.actions)
                
                # Files should still exist in original location
                for source, _ in organizer.actions:
                    assert source.exists()
    
    def test_execute_real_move(self, sample_files):
        """Test execute with real moves."""
        organizer = FileOrganizer(sample_files, dry_run=False)
        organizer.scan_and_plan()
        
        with patch('src.organizer.logger') as mock_logger:
            with patch('builtins.print') as mock_print:
                organizer.execute()
                
                # Should log move messages
                assert mock_logger.info.call_count == len(organizer.actions)
                # Should print messages
                assert mock_print.call_count == len(organizer.actions)
                
                # Files should be moved to category directories
                for source, dest in organizer.actions:
                    assert not source.exists()
                    assert dest.exists()
                    assert dest.parent.exists()
    
    def test_get_summary_no_actions(self):
        """Test get_summary with no actions."""
        organizer = FileOrganizer(Path("/tmp"), dry_run=True)
        summary = organizer.get_summary()
        assert summary == "No files to organize."
    
    def test_scan_and_plan_permission_error(self, temp_dir):
        """Test scan_and_plan with permission error."""
        # Create a directory and make it unreadable
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "file.txt").write_text("content")
        
        # Mock iterdir to raise PermissionError
        with patch.object(Path, 'iterdir', side_effect=PermissionError("Permission denied")):
            organizer = FileOrganizer(temp_dir, dry_run=True)
            with patch('src.organizer.logger') as mock_logger:
                organizer.scan_and_plan()
                mock_logger.error.assert_called_once()
                assert organizer.actions == []
    
    def test_execute_creates_category_directories(self, temp_dir):
        """Test that execute creates category directories."""
        pdf_file = temp_dir / "test.pdf"
        pdf_file.write_text("content")
        
        organizer = FileOrganizer(temp_dir, dry_run=False)
        organizer.scan_and_plan()
        organizer.execute()
        
        # PDF directory should be created
        pdf_dir = temp_dir / "PDF"
        assert pdf_dir.exists()
        assert pdf_dir.is_dir()
        assert (pdf_dir / "test.pdf").exists()
    
    def test_execute_handles_existing_category_directory(self, temp_dir):
        """Test execute when category directory already exists."""
        # Create category directory beforehand
        pdf_dir = temp_dir / "PDF"
        pdf_dir.mkdir()
        existing_file = pdf_dir / "existing.pdf"
        existing_file.write_text("existing")
        
        # Add new file
        new_pdf = temp_dir / "new.pdf"
        new_pdf.write_text("new")
        
        organizer = FileOrganizer(temp_dir, dry_run=False)
        organizer.scan_and_plan()
        organizer.execute()
        
        # Both files should exist
        assert existing_file.exists()
        assert (pdf_dir / "new.pdf").exists()
    
    def test_get_summary_category_counts(self, temp_dir):
        """Test get_summary provides accurate category counts."""
        # Create multiple files in same category
        (temp_dir / "doc1.pdf").write_text("content")
        (temp_dir / "doc2.pdf").write_text("content")
        (temp_dir / "script.py").write_text("code")
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer.scan_and_plan()
        summary = organizer.get_summary()
        
        assert "PDF: 2 files" in summary
        assert "Code: 1 files" in summary
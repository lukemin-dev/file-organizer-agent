import pytest
import os
import stat
from pathlib import Path
from unittest.mock import patch
from src.organizer import FileOrganizer

class TestEdgeCases:
    def test_hidden_files(self, temp_dir):
        """Test that hidden files (starting with .) are ignored."""
        hidden_file = temp_dir / ".hidden.txt"
        hidden_file.write_text("hidden content")
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer.scan_and_plan()
        
        # Hidden files should be ignored
        assert len(organizer.actions) == 0
    
    def test_files_without_extension(self, temp_dir):
        """Test handling of files without extension."""
        no_ext_file = temp_dir / "README"
        no_ext_file.write_text("readme content")
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer.scan_and_plan()
        
        assert len(organizer.actions) == 1
        source, dest = organizer.actions[0]
        assert source == no_ext_file
        assert dest.parent.name == "Others"
        assert dest.name == "README"
    
    def test_files_with_multiple_dots(self, temp_dir):
        """Test handling of files with multiple dots in name."""
        multi_dot_file = temp_dir / "file.name.with.dots.txt"
        multi_dot_file.write_text("content")
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer.scan_and_plan()
        
        assert len(organizer.actions) == 1
        source, dest = organizer.actions[0]
        assert source == multi_dot_file
        assert dest.parent.name == "Docs"  # .txt extension
        assert dest.name == "file.name.with.dots.txt"
    
    def test_empty_files(self, temp_dir):
        """Test handling of empty files."""
        empty_file = temp_dir / "empty.pdf"
        empty_file.write_text("")
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer.scan_and_plan()
        
        assert len(organizer.actions) == 1
        source, dest = organizer.actions[0]
        assert source == empty_file
        assert dest.parent.name == "PDF"
    
    def test_large_files(self, temp_dir):
        """Test handling of large files."""
        large_file = temp_dir / "large.zip"
        # Create a file with some content (simulating large file)
        large_content = "x" * 10000
        large_file.write_text(large_content)
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer.scan_and_plan()
        
        assert len(organizer.actions) == 1
        source, dest = organizer.actions[0]
        assert source == large_file
        assert dest.parent.name == "Archives"
    
    def test_files_with_special_characters(self, temp_dir):
        """Test handling of files with special characters in name."""
        special_file = temp_dir / "file with spaces & symbols.pdf"
        special_file.write_text("content")
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer.scan_and_plan()
        
        assert len(organizer.actions) == 1
        source, dest = organizer.actions[0]
        assert source == special_file
        assert dest.parent.name == "PDF"
        assert dest.name == "file with spaces & symbols.pdf"
    
    def test_unicode_filenames(self, temp_dir):
        """Test handling of files with unicode characters in name."""
        unicode_file = temp_dir / "файл_с_русскими_буквами.pdf"
        unicode_file.write_text("content")
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer.scan_and_plan()
        
        assert len(organizer.actions) == 1
        source, dest = organizer.actions[0]
        assert source == unicode_file
        assert dest.parent.name == "PDF"
        assert dest.name == "файл_с_русскими_буквами.pdf"
    
    def test_very_long_filenames(self, temp_dir):
        """Test handling of files with very long names."""
        long_name = "a" * 200 + ".txt"
        long_file = temp_dir / long_name
        long_file.write_text("content")
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer.scan_and_plan()
        
        assert len(organizer.actions) == 1
        source, dest = organizer.actions[0]
        assert source == long_file
        assert dest.parent.name == "Docs"
        assert dest.name == long_name
    
    def test_files_with_only_dots(self, temp_dir):
        """Test handling of files with only dots in name."""
        if os.name == 'nt':
            pytest.skip("Windows does not allow creating a file named '...'.")

        dots_file = temp_dir / "..."
        dots_file.write_text("content")
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer.scan_and_plan()
        
        # Files starting with . are ignored
        assert len(organizer.actions) == 0
    
    def test_files_starting_with_dot_and_extension(self, temp_dir):
        """Test hidden files with extensions."""
        hidden_with_ext = temp_dir / ".config.json"
        hidden_with_ext.write_text("content")
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer.scan_and_plan()
        
        # Hidden files are ignored
        assert len(organizer.actions) == 0
    
    @pytest.mark.skipif(os.name != 'posix', reason="Unix permissions test")
    def test_read_only_files(self, temp_dir):
        """Test handling of read-only files."""
        readonly_file = temp_dir / "readonly.pdf"
        readonly_file.write_text("content")
        readonly_file.chmod(stat.S_IRUSR)  # Read-only
        
        organizer = FileOrganizer(temp_dir, dry_run=False)
        organizer.scan_and_plan()
        
        # Should still plan the move
        assert len(organizer.actions) == 1
        
        # For real move, it might succeed or fail due to permissions
        # We test that the plan works
        try:
            organizer.execute()
        except OSError:
            # Expected if move fails due to permissions
            pass
        
        # Try to restore permissions if file still exists
        if readonly_file.exists():
            readonly_file.chmod(stat.S_IRUSR | stat.S_IWUSR)
    
    def test_directories_ignored(self, temp_dir):
        """Test that directories are ignored during scanning."""
        # Create a file and a directory
        test_file = temp_dir / "test.pdf"
        test_file.write_text("content")
        
        test_dir = temp_dir / "test_dir"
        test_dir.mkdir()
        (test_dir / "nested_file.txt").write_text("nested")
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer.scan_and_plan()
        
        # Should only plan to move the file, not the directory
        assert len(organizer.actions) == 1
        source, dest = organizer.actions[0]
        assert source == test_file
    
    def test_symlinks(self, temp_dir):
        """Test handling of symbolic links."""
        # Create target file
        target_file = temp_dir / "target.pdf"
        target_file.write_text("content")
        
        # Create symlink
        link_file = temp_dir / "link.pdf"
        try:
            link_file.symlink_to(target_file)
        except OSError as exc:
            pytest.skip(f"Symlink creation is not available in this environment: {exc}")
        
        organizer = FileOrganizer(temp_dir, dry_run=True)
        organizer.scan_and_plan()
        
        # Should plan to move both the real file and the symlink
        assert len(organizer.actions) == 2
        
        # Find the symlink action
        link_action = None
        for source, dest in organizer.actions:
            if source == link_file:
                link_action = (source, dest)
                break
        
        assert link_action is not None
        source, dest = link_action
        assert dest.parent.name == "PDF"
    
    def test_nonexistent_target_directory(self):
        """Test behavior with nonexistent target directory."""
        nonexistent = Path("/definitely/does/not/exist")
        organizer = FileOrganizer(nonexistent, dry_run=True)
        
        with patch('src.organizer.logger') as mock_logger:
            organizer.scan_and_plan()
            mock_logger.warning.assert_called_once_with(f"Target directory {nonexistent} does not exist.")
            assert organizer.actions == []
    
    def test_target_directory_with_no_read_permission(self, temp_dir):
        """Test behavior when target directory has no read permission."""
        # Create a subdirectory and remove read permission
        subdir = temp_dir / "no_read"
        subdir.mkdir()
        (subdir / "file.pdf").write_text("content")
        
        # Remove read permission from subdir
        if os.name == 'posix':
            subdir.chmod(0o000)
            try:
                with patch('src.organizer.logger') as mock_logger:
                    organizer = FileOrganizer(subdir, dry_run=True)
                    organizer.scan_and_plan()
                    mock_logger.error.assert_called_once()
                    assert organizer.actions == []  # No actions planned due to permission error
            finally:
                subdir.chmod(0o755)  # Restore permissions for cleanup

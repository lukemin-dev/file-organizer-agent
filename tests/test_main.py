import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import argparse
from src.main import main, setup_logging

class TestSetupLogging:
    def test_setup_logging(self, temp_dir):
        """Test setup_logging function."""
        import logging
        initial_handlers = len(logging.getLogger().handlers)
        
        log_file = temp_dir / "test.log"
        setup_logging(log_file)
        
        # Check that handlers were added to the root logger
        root_logger = logging.getLogger()
        handlers = root_logger.handlers
        
        # Should have more handlers now
        assert len(handlers) > initial_handlers
        
        # Should have at least file and stream handlers
        file_handlers = [h for h in handlers if isinstance(h, logging.FileHandler)]
        stream_handlers = [h for h in handlers if isinstance(h, logging.StreamHandler)]
        
        assert len(file_handlers) >= 1
        assert len(stream_handlers) >= 1

class TestMain:
    def test_main_default_args(self, temp_dir):
        """Test main with default arguments."""
        with patch('sys.argv', ['main.py']):
            with patch('src.main.setup_logging') as mock_setup:
                with patch('src.main.FileOrganizer') as mock_organizer_class:
                    mock_organizer = MagicMock()
                    mock_organizer_class.return_value = mock_organizer
                    mock_organizer.get_summary.return_value = "Test summary"
                    
                    with patch('builtins.print') as mock_print:
                        main()
                        
                        # Check setup_logging called
                        mock_setup.assert_called_once()
                        
                        # Check FileOrganizer created with default target and dry_run=True
                        mock_organizer_class.assert_called_once()
                        args, kwargs = mock_organizer_class.call_args
                        assert kwargs['dry_run'] is True
                        
                        # Check scan_and_plan called
                        mock_organizer.scan_and_plan.assert_called_once()
                        
                        # Check get_summary called and printed
                        mock_organizer.get_summary.assert_called_once()
                        mock_print.assert_called_once_with("Test summary")
    
    def test_main_with_target_and_apply(self, temp_dir):
        """Test main with custom target and apply flag."""
        target_dir = temp_dir / "custom"
        with patch('sys.argv', ['main.py', '--target', str(target_dir), '--apply']):
            with patch('src.main.setup_logging'):
                with patch('src.main.FileOrganizer') as mock_organizer_class:
                    mock_organizer = MagicMock()
                    mock_organizer_class.return_value = mock_organizer
                    
                    main()
                    
                    # Check FileOrganizer created with custom target and dry_run=False
                    mock_organizer_class.assert_called_once()
                    args, kwargs = mock_organizer_class.call_args
                    assert args[0] == target_dir
                    assert kwargs['dry_run'] is False
    
    def test_main_with_invalid_target(self):
        """Test main with invalid target argument."""
        with patch('sys.argv', ['main.py', '--target', 'invalid/path']):
            with patch('src.main.setup_logging'):
                with patch('src.main.FileOrganizer') as mock_organizer_class:
                    # Should still work as Path can handle invalid paths
                    mock_organizer = MagicMock()
                    mock_organizer_class.return_value = mock_organizer
                    
                    main()
                    
                    # Check FileOrganizer created
                    mock_organizer_class.assert_called_once()
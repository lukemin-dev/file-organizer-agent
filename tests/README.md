# Test Suite for File Organizer

This directory contains comprehensive tests for the Python file organizer program.

## Test Structure

- `conftest.py` - Pytest fixtures and configuration
- `test_config.py` - Unit tests for configuration module
- `test_utils.py` - Unit tests for utility functions
- `test_organizer.py` - Unit tests for FileOrganizer class
- `test_main.py` - Unit tests for main module
- `test_integration.py` - Integration tests
- `test_edge_cases.py` - Edge case and error handling tests

## Running Tests

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run Specific Test Files
```bash
pytest test_config.py
pytest test_utils.py
pytest test_organizer.py
pytest test_main.py
pytest test_integration.py
pytest test_edge_cases.py
```

### Run with Coverage
```bash
pip install pytest-cov
pytest --cov=src --cov-report=html
```

### Run Tests Verbose
```bash
pytest -v
```

## Test Categories

### Unit Tests
- Test individual functions and methods in isolation
- Mock external dependencies
- Fast execution

### Integration Tests
- Test complete workflows
- Test interaction between components
- Use real file system operations

### Edge Case Tests
- Test error conditions
- Test boundary cases
- Test unusual file types and permissions

## Test Data

Tests use temporary directories and sample files created via fixtures:
- PDF files (.pdf)
- Document files (.docx, .txt)
- Image files (.jpg)
- Archive files (.zip)
- Code files (.py)
- Data files (.csv)
- Unknown extensions (.xyz)
- Files without extensions
- Hidden files (starting with .)

## Fixtures

- `temp_dir` - Temporary directory for testing
- `sample_files` - Pre-populated directory with test files

## Test Runner Configuration

See `pytest.ini` for configuration:
- Verbose output
- Short traceback format
- Test discovery patterns
- Custom markers

## Manual Testing

See `MANUAL_TESTING.md` for manual testing procedures and additional validation steps.
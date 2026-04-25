# Manual Testing Procedures for File Organizer

This document outlines manual testing procedures to validate the file organizer program functionality.

## Prerequisites

1. Python 3.7+ installed
2. pytest installed (`pip install pytest`)
3. Sample files created in test directory

## Test Environment Setup

1. Create a test directory with sample files:
   ```bash
   mkdir test_downloads
   cd test_downloads
   echo "PDF content" > document.pdf
   echo "Presentation content" > slides.pptx
   echo "Document content" > text.docx
   echo "Image content" > photo.jpg
   echo "Installer content" > setup.exe
   echo "Archive content" > backup.zip
   echo "Code content" > script.py
   echo "Data content" > data.csv
   echo "Unknown content" > unknown.xyz
   echo "No extension content" > README
   echo "Hidden content" > .hidden
   ```

## Test Cases

### 1. Basic Functionality Test

**Objective:** Verify basic file organization works correctly.

**Steps:**
1. Run the organizer in dry-run mode:
   ```bash
   python -m src.main --target test_downloads
   ```
2. Verify output shows planned moves without actually moving files
3. Check that all files are still in `test_downloads`
4. Run with apply flag:
   ```bash
   python -m src.main --target test_downloads --apply
   ```
5. Verify files have been moved to appropriate category subdirectories

**Expected Results:**
- Dry run: Files remain in place, summary shows planned organization
- Apply: Files moved to `PDF/`, `Slides/`, `Docs/`, etc. directories

### 2. Default Target Directory Test

**Objective:** Verify default target directory (~/Downloads) is used when no target specified.

**Steps:**
1. Create sample files in ~/Downloads
2. Run: `python -m src.main`
3. Verify files in ~/Downloads are organized

**Expected Results:**
- Files in ~/Downloads organized into categories

### 3. Logging Test

**Objective:** Verify logging functionality works correctly.

**Steps:**
1. Run organizer on test directory
2. Check logs/organizer.log file is created
3. Verify log contains appropriate INFO level messages
4. Check console output for user-friendly messages

**Expected Results:**
- Log file created with timestamped entries
- Console shows progress messages

### 4. Error Handling Test

**Objective:** Verify error handling for edge cases.

**Steps:**
1. Try to organize a non-existent directory:
   ```bash
   python -m src.main --target /nonexistent/path
   ```
2. Create a read-only file and try to organize:
   ```bash
   echo "content" > readonly.pdf
   chmod 444 readonly.pdf
   python -m src.main --target . --apply
   ```
3. Try organizing an empty directory

### 5. Permission and Access Test

**Objective:** Verify handling of files with restricted permissions.

**Steps:**
1. Create test files with different permissions:
   ```bash
   echo "content" > normal.pdf
   echo "content" > readonly.pdf && chmod 444 readonly.pdf
   echo "content" > executable.pdf && chmod 755 executable.pdf
   ```
2. Run organizer: `python -m src.main --target . --apply`
3. Check logs for any permission-related errors
4. Verify that accessible files are moved and inaccessible ones are handled gracefully

**Expected Results:**
- Normal files: Moved successfully
- Read-only files: May fail to move, appropriate error logged
- No crashes or hangs

### 6. Large Directory Test

**Objective:** Test performance with many files.

**Steps:**
1. Create many test files:
   ```bash
   for i in {1..100}; do echo "content $i" > "file_$i.pdf"; done
   ```
2. Run organizer and measure time:
   ```bash
   time python -m src.main --target . --apply
   ```
3. Verify all files are organized correctly

**Expected Results:**
- All files organized into appropriate categories
- Reasonable execution time (< 30 seconds for 100 files)

### 7. Network/Remote Directory Test

**Objective:** Test with network-mounted or remote directories.

**Steps:**
1. If available, test with a network share or external drive
2. Run organizer on the remote directory
3. Verify files are organized correctly

**Expected Results:**
- Same behavior as local directories
- Appropriate error handling if network issues occur

### 8. Concurrent Access Test

**Objective:** Test behavior when files are accessed by other processes.

**Steps:**
1. Create test files
2. Open one file in another program (e.g., text editor)
3. Run organizer while file is open
4. Try to organize again after closing the file

**Expected Results:**
- Files that are locked: May fail to move, appropriate error handling
- Other files: Moved successfully
- No corruption of locked files

### 9. Undo/Recovery Test

**Objective:** Test recovery from failed operations.

**Steps:**
1. Run organizer with `--apply`
2. Simulate failure (e.g., interrupt during execution)
3. Check state of files and logs
4. Re-run organizer to complete organization

**Expected Results:**
- Partial moves are logged
- Re-running completes the organization
- No duplicate files created

### 10. Configuration Validation Test

**Objective:** Verify configuration changes work correctly.

**Steps:**
1. Modify `src/config.py` to add new category:
   ```python
   CATEGORIES["Videos"] = ["mp4", "avi", "mkv"]
   ```
2. Create test video file: `echo "video" > test.mp4`
3. Run organizer
4. Verify file goes to Videos category

**Expected Results:**
- New category created
- File organized correctly

## Automated Test Execution

### Running Unit Tests
```bash
pytest tests/test_config.py -v
pytest tests/test_utils.py -v
pytest tests/test_organizer.py -v
pytest tests/test_main.py -v
```

### Running Integration Tests
```bash
pytest tests/test_integration.py -v
```

### Running Edge Case Tests
```bash
pytest tests/test_edge_cases.py -v
```

### Running All Tests
```bash
pytest
```

### Running Tests with Coverage
```bash
pip install pytest-cov
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## Test Data Setup

### Sample Files Creation Script
```bash
#!/bin/bash
# create_sample_files.sh
mkdir -p test_data
cd test_data

# Create sample files for each category
echo "PDF document content" > sample.pdf
echo "PowerPoint content" > presentation.pptx
echo "Word document content" > document.docx
echo "Text file content" > notes.txt
echo "Image content" > photo.jpg
echo "Installer content" > setup.exe
echo "Archive content" > backup.zip
echo "Python code" > script.py
echo "CSV data" > data.csv
echo "Unknown format" > mystery.xyz
echo "No extension file" > README
echo "Hidden file" > .config

# Create edge case files
echo "content" > "file with spaces.pdf"
echo "content" > "file-with-dashes.pdf"
echo "content" > "file_with_underscores.pdf"
echo "content" > "file.with.multiple.dots.pdf"
echo "content" > ".hidden.pdf"
echo "content" > "UPPERCASE.PDF"
echo "content" > "MixedCase.TxT"

# Create duplicate names for testing
echo "duplicate 1" > duplicate.pdf
mkdir PDF && echo "duplicate 2" > PDF/duplicate.pdf
```

### Cleanup Script
```bash
#!/bin/bash
# cleanup_test_data.sh
rm -rf test_data
rm -f logs/*.log
```

### 5. File Type Recognition Test

**Objective:** Verify all file extensions are correctly categorized.

**Steps:**
1. Create files with various extensions
2. Run organizer
3. Check each file is moved to correct category directory

**Expected Results:**
- PDF files → PDF/
- .pptx, .ppt, .odp → Slides/
- .docx, .doc, .odt, .txt → Docs/
- .jpg, .jpeg, .png, .gif, .bmp, .tiff → Images/
- .exe, .msi, .dmg, .pkg → Installers/
- .zip, .rar, .7z, .tar, .gz → Archives/
- .py, .js, .html, .css, .java, .cpp, .c, .h → Code/
- .csv, .xlsx, .xls, .json, .xml → Data/
- Unknown extensions → Others/

### 6. Duplicate Filename Handling Test

**Objective:** Verify duplicate filenames are handled with unique names.

**Steps:**
1. Create two files with same name but different extensions that go to same category
2. Or create files that would result in same target path
3. Run organizer
4. Check files get unique names like `filename_1.ext`

**Expected Results:**
- No filename conflicts, unique names assigned

### 7. Hidden Files Test

**Objective:** Verify hidden files (starting with .) are handled correctly.

**Steps:**
1. Create hidden files: `.hidden.txt`, `.config`
2. Run organizer
3. Check hidden files are categorized and moved appropriately

**Expected Results:**
- Hidden files processed same as regular files

### 8. Permission Test

**Objective:** Verify behavior with permission issues.

**Steps:**
1. Create files with various permissions
2. Set some files as read-only
3. Try to organize
4. Check error handling

**Expected Results:**
- Appropriate error messages for permission issues
- Program doesn't crash

### 9. Large Directory Test

**Objective:** Verify performance with many files.

**Steps:**
1. Create directory with 100+ files of various types
2. Run organizer
3. Time the operation
4. Verify all files organized correctly

**Expected Results:**
- All files organized correctly
- Reasonable performance (< 1 minute for 100 files)

### 10. Undo Operation Test

**Objective:** Test ability to undo organization (manual process).

**Steps:**
1. Organize files
2. Manually move files back to root directory
3. Verify structure is restored

**Expected Results:**
- Manual undo works correctly

## Automated Test Execution

Run all tests:
```bash
pytest
```

Run specific test categories:
```bash
pytest tests/test_unit.py
pytest tests/test_integration.py
pytest tests/test_edge_cases.py
```

Run with coverage:
```bash
pip install pytest-cov
pytest --cov=src --cov-report=html
```

## Performance Benchmarks

- Small directory (10 files): < 1 second
- Medium directory (100 files): < 10 seconds
- Large directory (1000 files): < 2 minutes

## Cleanup

After testing:
```bash
rm -rf test_downloads
rm -rf logs/*.log
```
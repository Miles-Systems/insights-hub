# Phase 0 - Python PDF Reader Development Log

## Project goal

Build a small Python project that can read text from PDF files in the sample folder, separate the PDF-reading logic from the entry point, and make the script user-friendly for learning purposes.

## Development iterations

### 1. Initial PDF reading prototype

- Started with a simple script that used the pypdf library.
- The first version read a PDF file directly from a known path.
- This was useful for learning the basic API.

### 2. Switching to a project-relative path

- Replaced a home-folder-based path with a path built from the project structure.
- The code used pathlib to locate the PDF reliably from the repository root.
- This made the script more portable across machines.

### 3. Reading page content

- Learned how to access pages from the PDF reader object.
- Tried both:
  - reading only the first page, and
  - looping through all pages.
- The loop-based approach became the main pattern for reading all pages.

### 4. Separating responsibilities into modules

- Moved the PDF-reading logic into a dedicated module:
  - app/reader.py
- Kept the script entry point in:
  - app/main.py
- This introduced the beginner-friendly idea of:
  - reader.py = how to read the PDF
  - main.py = how to use that logic

### 5. Accepting a file path from the terminal

- Updated the entry point to read a file path from the command line using sys.argv.
- This made the program more flexible because the user could provide a PDF path at runtime.

### 6. Adding a usage hint

- When no file path was provided, the program printed a friendly message instead of silently using a default.
- This helped teach command-line input and error messaging.

### 7. Adding basic exception handling

- Added handling for:
  - missing files
  - PDFs with no extractable text
- This improved the experience and showed how to handle runtime problems gracefully.

### 8. Preparing the project for package-style structure

- Added an **init**.py file in the app folder.
- Switched imports to package-style imports such as:
  - from app.reader import read_pdf
- This is a step toward making the project feel more like a real Python package.
  Note: use -m flag to let Python know to run a module by module name.

### 9. Repository hygiene

- Added a .gitignore file to ignore Python cache artifacts such as:
  - **pycache**/
  - \*.pyc

## Current structure

- app/main.py
  - entry point for the script
  - collects the PDF path from the terminal
  - handles user-friendly errors
- app/reader.py
  - contains the PDF extraction logic
  - checks for missing files and empty/no-text PDFs
- sample/
  - contains sample PDF files used for testing
- docs/
  - documentation files for the project

## How to run the script

From the project root, use:

```bash
python -m app.main sample/minimal-document.pdf
```

If you want to run it as a direct script file instead:

```bash
python app/main.py sample/minimal-document.pdf
```

## Key concepts learned

- pathlib for file paths
- loops for reading page-by-page content
- functions for separating logic
- sys.argv for command-line arguments
- exception handling with try/except
- package-style imports with **init**.py
- basic project organization and documentation

## Notes for future improvements

- Add support for selecting a specific page number.
- Add support for saving extracted text to a .txt file.
- Add tests for missing files and blank PDFs.
- Consider packaging the project properly with a setup file if it grows further.

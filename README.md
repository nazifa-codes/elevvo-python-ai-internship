# Elevvo Pathways | Python Programming & AI
## Selected Internship Tasks

This repository contains four projects selected from the official **Python Programming & AI Tasks** PDF:

1. **Task 1: CLI Expense Tracker with Persistent Storage** (Level 1)
2. **Task 2: Student Grade Processor with Custom Functions** (Level 1)
3. **Task 3: Automated File Organizer** (Level 2)
4. **Task 4: Object-Oriented Inventory Management System** (Level 2)

All four projects are implemented with Python. The projects include the required core features and selected bonus features.

## Requirements
- Python 3.10 or newer
- No third-party packages are required.

## Run a project
Open Command Prompt in the relevant task folder and run the command shown in that folder's README.

## Project structure
- `task1_expense_tracker/` - JSON-backed CLI expense tracker and monthly category report.
- `task2_grade_processor/` - importable grade-processing module, validation, custom exception, and type hints.
- `task3_file_organizer/` - safe extension-based file organizer, collision handling, logging, and dry-run.
- `task4_inventory_system/` - Product and PerishableProduct classes, stock validation, expiry alerts, and reports.

## Testing
Each project includes tests using Python's built-in `unittest` framework. Run the tests from each project folder with:

```bash
python -m unittest -v
```

## Notes
- Task 3 does not overwrite destination files. Conflicting names receive a numbered suffix.
- Task 4's PerishableProduct subclass adds expiry-date behavior.
- Task 1 stores data in a local JSON file. The sample data file is intentionally empty so each user starts with a clean tracker.
- Task 5 and above were not selected for this submission.

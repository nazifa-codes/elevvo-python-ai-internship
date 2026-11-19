# Task 3: Automated File Organizer

### Required features
- Scans a target directory and sorts files into extension-based folders.
- Never overwrites a destination file. Conflicts receive numbered names.
- Prints a summary of each move.
- Handles missing folders, empty folders, and permission/OS errors.

### Included bonus
- File logging and `--dry-run` preview mode.

### Run
```bash
python file_organizer.py "C:\path\to\folder" --dry-run
python file_organizer.py "C:\path\to\folder"
```

Use `--log organizer.log` to choose a log file. The script skips its own log file.

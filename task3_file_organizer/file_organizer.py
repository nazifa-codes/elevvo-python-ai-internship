"""Safely organize files into folders named by file extension."""
import argparse
import logging
import shutil
from pathlib import Path


def unique_destination(destination: Path) -> Path:
    """Return a non-existing destination path without overwriting anything."""
    if not destination.exists():
        return destination
    parent, stem, suffix = destination.parent, destination.stem, destination.suffix
    counter = 1
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def organize_directory(target: Path, dry_run: bool = False,
                       log_path: Path | None = None) -> list[dict]:
    """Organize direct child files by extension and return operation records."""
    target = target.expanduser().resolve()
    if not target.exists():
        raise FileNotFoundError(f"Target directory does not exist: {target}")
    if not target.is_dir():
        raise NotADirectoryError(f"Target is not a directory: {target}")

    operations = []
    for source in sorted(target.iterdir()):
        if not source.is_file():
            continue
        if log_path and source.resolve() == log_path.expanduser().resolve():
            continue

        extension = source.suffix.lower().lstrip(".") or "no_extension"
        destination_folder = target / extension
        destination = unique_destination(destination_folder / source.name)
        record = {
            "filename": source.name,
            "source": str(source),
            "destination": str(destination),
            "status": "preview" if dry_run else "moved",
        }
        try:
            if not dry_run:
                destination_folder.mkdir(exist_ok=True)
                destination = unique_destination(destination_folder / source.name)
                record["destination"] = str(destination)
                shutil.move(str(source), str(destination))
            operations.append(record)
            print(f'{record["status"].upper()}: {record["filename"]}')
            print(f'  From: {record["source"]}')
            print(f'  To:   {record["destination"]}')
        except (PermissionError, OSError) as error:
            record["status"] = "error"
            record["error"] = str(error)
            operations.append(record)
            print(f"ERROR: Could not move {source.name}: {error}")
    if not operations:
        print("No files found to organize.")
    return operations


def main() -> None:
    parser = argparse.ArgumentParser(description="Organize files by extension safely.")
    parser.add_argument("directory", type=Path, help="Directory to organize")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview operations without moving files")
    parser.add_argument("--log", type=Path, default=Path("organizer.log"),
                        help="Path to the operation log (default: organizer.log)")
    args = parser.parse_args()

    logging.basicConfig(
        filename=args.log, level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
    try:
        operations = organize_directory(args.directory, args.dry_run, args.log)
        for operation in operations:
            logging.info("%s | %s | %s",
                         operation["status"], operation["source"],
                         operation["destination"])
    except (FileNotFoundError, NotADirectoryError, PermissionError) as error:
        print(f"Cannot organize directory: {error}")
        logging.error("%s", error)


if __name__ == "__main__":
    main()

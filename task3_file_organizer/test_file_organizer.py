import tempfile
import unittest
from pathlib import Path
from file_organizer import organize_directory, unique_destination


class FileOrganizerTests(unittest.TestCase):
    def test_moves_files_into_extension_folder(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "notes.txt"
            source.write_text("hello", encoding="utf-8")
            result = organize_directory(root)
            self.assertEqual(result[0]["status"], "moved")
            self.assertTrue((root / "txt" / "notes.txt").exists())
            self.assertFalse(source.exists())

    def test_collision_gets_numbered_name(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            destination = root / "txt" / "notes.txt"
            destination.parent.mkdir()
            destination.write_text("existing", encoding="utf-8")
            candidate = unique_destination(destination)
            self.assertEqual(candidate.name, "notes_1.txt")
            self.assertTrue(destination.exists())

    def test_dry_run_does_not_move(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "image.png"
            source.write_bytes(b"data")
            result = organize_directory(root, dry_run=True)
            self.assertEqual(result[0]["status"], "preview")
            self.assertTrue(source.exists())
            self.assertFalse((root / "png").exists())

    def test_missing_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError):
                organize_directory(Path(folder) / "missing")


if __name__ == "__main__":
    unittest.main()

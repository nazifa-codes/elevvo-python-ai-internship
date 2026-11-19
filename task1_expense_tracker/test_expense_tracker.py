import tempfile
import unittest
from pathlib import Path
from expense_tracker import add_expense, load_expenses, save_expenses, monthly_summary


class ExpenseTrackerTests(unittest.TestCase):
    def test_add_and_persist(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "expenses.json"
            expenses = []
            add_expense(expenses, 120.50, "food", "2026-11-19")
            save_expenses(expenses, path)
            self.assertEqual(load_expenses(path)[0]["category"], "Food")

    def test_reject_invalid_amount(self):
        with self.assertRaises(ValueError):
            add_expense([], 0, "Food", "2026-11-19")

    def test_monthly_summary(self):
        expenses = [
            {"amount": 100.0, "category": "Food", "date": "2026-11-01"},
            {"amount": 50.0, "category": "Food", "date": "2026-11-15"},
            {"amount": 40.0, "category": "Travel", "date": "2026-10-15"},
        ]
        report = monthly_summary(expenses, "2026-11")
        self.assertEqual(report["total"], 150.0)
        self.assertEqual(report["category_averages"]["Food"], 75.0)


if __name__ == "__main__":
    unittest.main()

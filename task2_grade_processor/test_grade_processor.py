import unittest
from grade_processor import (
    InvalidScoreError, average_score, highest_score, lowest_score,
    pass_fail_status, process_students
)


class GradeProcessorTests(unittest.TestCase):
    def setUp(self):
        self.students = [
            {"name": "Amina", "score": 85},
            {"name": "Rafi", "score": 35},
            {"name": "Nila", "score": 70},
        ]

    def test_statistics(self):
        self.assertAlmostEqual(average_score(self.students), 190 / 3)
        self.assertEqual(highest_score(self.students), 85)
        self.assertEqual(lowest_score(self.students), 35)

    def test_pass_fail(self):
        self.assertEqual(pass_fail_status(40), "Pass")
        self.assertEqual(pass_fail_status(39.9), "Fail")

    def test_invalid_score(self):
        with self.assertRaises(InvalidScoreError):
            average_score([{"name": "Bad", "score": 101}])

    def test_empty_list(self):
        self.assertEqual(average_score([]), 0.0)
        self.assertIsNone(highest_score([]))
        self.assertIsNone(lowest_score([]))

    def test_full_report(self):
        report = process_students(self.students)
        self.assertEqual(report["statuses"]["Rafi"], "Fail")


if __name__ == "__main__":
    unittest.main()

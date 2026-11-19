"""Reusable functions for validating and processing student grades."""
from typing import TypedDict


class InvalidScoreError(ValueError):
    """Raised when a score is outside the allowed range or not numeric."""


class Student(TypedDict):
    name: str
    score: float


PASS_MARK = 40.0


def validate_score(score: float) -> float:
    """Return a valid score as float; reject values outside 0..100."""
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise InvalidScoreError("Score must be a number.")
    if not 0 <= score <= 100:
        raise InvalidScoreError("Score must be between 0 and 100.")
    return float(score)


def average_score(students: list[Student]) -> float:
    """Calculate the mean score. Return 0.0 for an empty list."""
    if not students:
        return 0.0
    scores = [validate_score(student["score"]) for student in students]
    return sum(scores) / len(scores)


def highest_score(students: list[Student]) -> float | None:
    """Return the highest score, or None if there are no students."""
    return max((validate_score(s["score"]) for s in students), default=None)


def lowest_score(students: list[Student]) -> float | None:
    """Return the lowest score, or None if there are no students."""
    return min((validate_score(s["score"]) for s in students), default=None)


def pass_fail_status(score: float, pass_mark: float = PASS_MARK) -> str:
    """Return Pass or Fail after validating score and pass mark."""
    score = validate_score(score)
    pass_mark = validate_score(pass_mark)
    return "Pass" if score >= pass_mark else "Fail"


def process_students(students: list[Student]) -> dict:
    """Create a summary containing average, highest, lowest, and statuses."""
    for student in students:
        if not student.get("name", "").strip():
            raise ValueError("Every student must have a name.")
        validate_score(student["score"])
    return {
        "average": average_score(students),
        "highest": highest_score(students),
        "lowest": lowest_score(students),
        "statuses": {
            student["name"]: pass_fail_status(student["score"])
            for student in students
        },
    }

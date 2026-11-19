"""Demonstration CLI for the grade processor."""
from grade_processor import InvalidScoreError, process_students

def main() -> None:
    students = []
    print("Enter student records. Leave the name blank to finish.")
    while True:
        name = input("Student name: ").strip()
        if not name:
            break
        try:
            score = float(input("Score (0-100): "))
            students.append({"name": name, "score": score})
        except ValueError:
            print("Please enter a valid numeric score.")
    try:
        report = process_students(students)
    except (InvalidScoreError, ValueError) as error:
        print(f"Could not process grades: {error}")
        return

    print("\n=== Grade Report ===")
    print(f'Average: {report["average"]:.2f}')
    print(f'Highest: {report["highest"]}')
    print(f'Lowest: {report["lowest"]}')
    for name, status in report["statuses"].items():
        print(f"{name}: {status}")


if __name__ == "__main__":
    main()

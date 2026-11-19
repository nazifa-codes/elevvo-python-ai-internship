"""A small command-line expense tracker backed by a JSON file."""
import json
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.json")


def load_expenses(file_path: Path = DATA_FILE) -> list[dict]:
    """Load expenses from JSON, returning an empty list if no file exists."""
    if not file_path.exists():
        return []
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Expense file contains invalid JSON: {file_path}") from exc
    if not isinstance(data, list):
        raise ValueError("Expense data must be a JSON list.")
    return data


def save_expenses(expenses: list[dict], file_path: Path = DATA_FILE) -> None:
    """Persist expenses to a JSON file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(expenses, indent=4), encoding="utf-8")


def add_expense(expenses: list[dict], amount: float, category: str,
                expense_date: str) -> dict:
    """Validate and append one expense entry."""
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if not category.strip():
        raise ValueError("Category cannot be empty.")
    try:
        date.fromisoformat(expense_date)
    except ValueError as exc:
        raise ValueError("Date must be a valid YYYY-MM-DD date.") from exc

    entry = {
        "amount": round(float(amount), 2),
        "category": category.strip().title(),
        "date": expense_date,
    }
    expenses.append(entry)
    return entry


def monthly_summary(expenses: list[dict], year_month: str) -> dict:
    """Return total and per-category totals/averages for YYYY-MM."""
    try:
        date.fromisoformat(year_month + "-01")
    except ValueError as exc:
        raise ValueError("Month must use YYYY-MM format.") from exc

    selected = [item for item in expenses if item["date"].startswith(year_month)]
    totals = {}
    counts = {}
    for item in selected:
        category = item["category"]
        totals[category] = totals.get(category, 0.0) + float(item["amount"])
        counts[category] = counts.get(category, 0) + 1

    averages = {key: totals[key] / counts[key] for key in totals}
    return {
        "month": year_month,
        "expense_count": len(selected),
        "total": sum(totals.values()),
        "category_totals": totals,
        "category_averages": averages,
    }


def main() -> None:
    try:
        expenses = load_expenses()
    except ValueError as error:
        print(f"Could not load saved expenses: {error}")
        return

    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add expense\n2. List expenses\n3. Monthly summary\n4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            try:
                amount = float(input("Amount: "))
                category = input("Category: ")
                expense_date = input("Date (YYYY-MM-DD): ").strip()
                entry = add_expense(expenses, amount, category, expense_date)
                save_expenses(expenses)
                print(f"Saved: {entry}")
            except ValueError as error:
                print(f"Invalid expense: {error}")
        elif choice == "2":
            if not expenses:
                print("No expenses recorded.")
            for item in expenses:
                print(f'{item["date"]} | {item["category"]} | {item["amount"]:.2f}')
        elif choice == "3":
            try:
                report = monthly_summary(expenses, input("Month (YYYY-MM): ").strip())
                print(f'\nSummary for {report["month"]}')
                print(f'Total expenses: {report["expense_count"]}')
                print(f'Total spending: {report["total"]:.2f}')
                for category, total in report["category_totals"].items():
                    average = report["category_averages"][category]
                    print(f"{category}: total={total:.2f}, average={average:.2f}")
            except ValueError as error:
                print(error)
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()

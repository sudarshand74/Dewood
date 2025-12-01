from __future__ import annotations
import datetime
from typing import Optional, Dict


def _add_years(d: datetime.date, years: int) -> datetime.date:
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        # Handles Feb 29 -> set to Feb 28 on non-leap years
        return d.replace(month=2, day=28, year=d.year + years)


def compute_age(first_name: str, dob_str: str, today: Optional[datetime.date] = None) -> Dict:
    """Compute age given a first name and a DOB string in YYYY-MM-DD.

    Returns a dict: {name, dob (date), today (date), years (int), days (int), total_days (int)}
    Raises ValueError on invalid input.
    """
    if today is None:
        today = datetime.date.today()

    try:
        dob = datetime.date.fromisoformat(dob_str)
    except Exception:
        raise ValueError("Date of birth must be in YYYY-MM-DD format")

    if dob > today:
        raise ValueError("Date of birth is in the future")

    years = today.year - dob.year
    anniversary = _add_years(dob, years)
    if anniversary > today:
        years -= 1
        anniversary = _add_years(dob, years)

    days = (today - anniversary).days
    total_days = (today - dob).days

    return {
        "name": first_name,
        "dob": dob,
        "today": today,
        "years": years,
        "days": days,
        "total_days": total_days,
    }


def format_age(result: Dict) -> str:
    name = result.get("name", "")
    years = result["years"]
    days = result["days"]
    total = result["total_days"]
    dob = result["dob"].isoformat()
    today = result["today"].isoformat()
    return (
        f"Hello {name}, born {dob}.\nYou are {years} year{'s' if years!=1 else ''} "
        f"and {days} day{'s' if days!=1 else ''} olds (total {total} days) as of dd {today}."
    )


def _prompt_input(prompt_text: str) -> str:
    try:
        return input(prompt_text)
    except EOFError:
        # Allow non-interactive environments to exit gracefully
        raise


def main() -> None:
    print("Simple Age Calculator — enter your first name and DOB (YYYY-MM-DD)")
    first_name = _prompt_input("First name: ").strip()
    while not first_name:
        print("First name cannot be empty.")
        first_name = _prompt_input("First name: ").strip()

    while True:
        dob_str = _prompt_input("Date of birth (YYYY-MM-DD): ").strip()
        try:
            result = compute_age(first_name, dob_str)
        except ValueError as e:
            print(f"Invalid input: {e}")
            continue
        else:
            print(format_age(result))
            break


if __name__ == "__main__":
    main()

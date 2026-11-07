from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

from habit_tracker.models import Habit
from habit_tracker.repository import HabitRepository
from habit_tracker.service import HabitService


DATABASE_PATH = Path("demo_habits.db")

START_DATE = date(2026, 10, 5)


def completion_timestamp(day):
    """Return a timestamp at 12:00 UTC for a calendar date."""

    return datetime.combine(
        day,
        time(12, 0),
        tzinfo=timezone.utc
    )


def main():
    """Create five predefined habits and four weeks of example data."""

    if DATABASE_PATH.exists():
        print("Demo database already exists.")
        print("Existing data was not changed.")
        return

    repository = HabitRepository(str(DATABASE_PATH))
    repository.initialize_database()

    service = HabitService(repository)

    habits = {
        "read": Habit("Read for 15 minutes", "daily"),
        "stretch": Habit("Stretch for 10 minutes", "daily"),
        "python": Habit("Practise Python for 20 minutes", "daily"),
        "plan": Habit("Plan the coming week", "weekly"),
        "call": Habit("Call a friend or relative", "weekly")
    }

    for habit in habits.values():
        habit.created_at = datetime(
            2026, 10, 5, 0, 0, tzinfo=timezone.utc
        )

        repository.save_habit(habit)


        stretch_missed = {
        date(2026, 10, 12),
        date(2026, 10, 22)
    }

    python_missed = {
        date(2026, 10, 9),
        date(2026, 10, 17),
        date(2026, 10, 26)
    }

    for day_number in range(28):
        current_day = START_DATE + timedelta(days=day_number)

        timestamp = completion_timestamp(current_day)

        repository.add_completion(
            habits["read"].id,
            timestamp
        )

        if current_day not in stretch_missed:
            repository.add_completion(
                habits["stretch"].id,
                timestamp
            )

        if current_day not in python_missed:
            repository.add_completion(
                habits["python"].id,
                timestamp
            )


    for week_number in range(4):
        monday = START_DATE + timedelta(weeks=week_number)

        repository.add_completion(
            habits["plan"].id,
            completion_timestamp(monday)
        )

        if week_number != 2:
            wednesday = monday + timedelta(days=2)

            repository.add_completion(
                habits["call"].id,
                completion_timestamp(wednesday)
            )


    print("\n===== FOUR-WEEK DEMONSTRATION DATA =====")

    for habit in repository.get_all_habits():
        streak = service.longest_streak_for_habit(habit.id)

        unit = "days" if habit.periodicity == "daily" else "weeks"

        print(f"\nHabit: {habit.task}")
        print(f"Periodicity: {habit.periodicity}")
        print(f"Longest streak: {streak} {unit}")

    overall = service.longest_streak_all_habits()

    print("\nLongest streak overall:", overall, "periods")
    print("Demonstration database created successfully!")


if __name__ == "__main__":
    main()
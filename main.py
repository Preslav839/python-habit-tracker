import argparse
import shutil
import tempfile

from pathlib import Path

from habit_tracker.repository import HabitRepository
from habit_tracker.service import HabitService
from habit_tracker.cli import run_cli


BASE_DIR = Path(__file__).resolve().parent


def start_tracker(database_path):
    """Initialize the database and start the application."""

    repository = HabitRepository(str(database_path))

    repository.initialize_database()

    service = HabitService(repository)

    try:
        run_cli(service)

    except (KeyboardInterrupt, EOFError):
        print("\nHabit Tracker closed.")


def main():
    """Start the Habit Tracker in normal or demonstration mode."""

    parser = argparse.ArgumentParser(
        description="Python Habit Tracker Application"
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Start the application using demonstration data"
    )

    args = parser.parse_args()

    if args.demo:

        demo_database = BASE_DIR / "demo_habits.db"

        if not demo_database.exists():
            print("Demonstration database not found.")
            print("Run: py -3.14 seed_demo.py")
            return

        with tempfile.TemporaryDirectory() as temporary_folder:

            temporary_database = (
                Path(temporary_folder) / "demo_session.db"
            )

            shutil.copyfile(
                demo_database,
                temporary_database
            )

            print("Starting Habit Tracker in DEMO mode.")
            print("Changes will not affect the original demo database.")

            start_tracker(temporary_database)

    else:

        normal_database = BASE_DIR / "habits.db"

        start_tracker(normal_database)


if __name__ == "__main__":
    main()
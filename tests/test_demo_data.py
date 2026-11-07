import io
import tempfile
import unittest

from contextlib import redirect_stdout
from datetime import date, timezone
from pathlib import Path
from unittest.mock import patch

import seed_demo

from habit_tracker.repository import HabitRepository
from habit_tracker.service import HabitService


class TestDemoFixtures(unittest.TestCase):
    """Test the predefined four-week habit dataset."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.database_path = (
            Path(self.temp_dir.name) / "demo_habits.db"
        )

        with patch.object(
            seed_demo, "DATABASE_PATH", self.database_path
        ):
            with redirect_stdout(io.StringIO()):
                seed_demo.main()

        self.repository = HabitRepository(
            str(self.database_path)
        )

        self.service = HabitService(self.repository)

        self.habits = {
            habit.task: habit
            for habit in self.repository.get_all_habits()
        }


    def test_five_predefined_habits(self):
        expected = {
            "Read for 15 minutes": "daily",
            "Stretch for 10 minutes": "daily",
            "Practise Python for 20 minutes": "daily",
            "Plan the coming week": "weekly",
            "Call a friend or relative": "weekly"
        }

        self.assertEqual(
            set(self.habits),
            set(expected)
        )

        for task, periodicity in expected.items():
            self.assertEqual(
                self.habits[task].periodicity,
                periodicity
            )


    def test_completion_counts(self):
        expected_counts = {
            "Read for 15 minutes": 28,
            "Stretch for 10 minutes": 26,
            "Practise Python for 20 minutes": 25,
            "Plan the coming week": 4,
            "Call a friend or relative": 3
        }

        total_completions = 0

        for task, expected_count in expected_counts.items():
            habit = self.habits[task]

            completions = self.repository.get_completions(
                habit.id
            )

            self.assertEqual(
                len(completions),
                expected_count
            )

            total_completions += len(completions)

        self.assertEqual(total_completions, 86)


    def test_expected_streaks(self):
        expected_streaks = {
            "Read for 15 minutes": 28,
            "Stretch for 10 minutes": 10,
            "Practise Python for 20 minutes": 8,
            "Plan the coming week": 4,
            "Call a friend or relative": 2
        }

        for task, expected_streak in expected_streaks.items():
            habit = self.habits[task]

            result = self.service.longest_streak_for_habit(
                habit.id
            )

            self.assertEqual(result, expected_streak)

        self.assertEqual(
            self.service.longest_streak_all_habits(),
            28
        )


    def test_completion_dates(self):
        start_date = date(2026, 10, 5)
        end_date = date(2026, 11, 1)

        for habit in self.habits.values():
            completions = self.repository.get_completions(
                habit.id
            )

            for completed_at in completions:
                completion_date = completed_at.astimezone(
                    timezone.utc
                ).date()

                self.assertGreaterEqual(
                    completion_date,
                    start_date
                )

                self.assertLessEqual(
                    completion_date,
                    end_date
                )

                self.assertGreaterEqual(
                    completed_at,
                    habit.created_at
                )


    def test_seed_does_not_duplicate_data(self):
        with patch.object(
            seed_demo, "DATABASE_PATH", self.database_path
        ):
            with redirect_stdout(io.StringIO()):
                seed_demo.main()

        habits = self.repository.get_all_habits()

        total_completions = sum(
            len(self.repository.get_completions(habit.id))
            for habit in habits
        )

        self.assertEqual(len(habits), 5)
        self.assertEqual(total_completions, 86)
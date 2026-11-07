from datetime import datetime, timezone
import unittest
import tempfile

from pathlib import Path

from habit_tracker.repository import HabitRepository
from habit_tracker.service import HabitService


class TestHabitService(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        database_path = Path(self.temp_dir.name) / "test_service.db"

        self.repository = HabitRepository(str(database_path))
        self.repository.initialize_database()

        self.service = HabitService(self.repository)

    def test_create_habit(self):
        habit = self.service.create_habit(
            "Read for 15 minutes", "daily"
        )

        self.assertIsNotNone(habit.id)
        self.assertEqual(habit.task, "Read for 15 minutes")
        self.assertEqual(habit.periodicity, "daily")

        saved_habits = self.repository.get_all_habits()

        self.assertEqual(len(saved_habits), 1)

    def test_list_habits(self):
        self.service.create_habit(
            "Read for 15 minutes", "daily"
        )

        self.service.create_habit(
            "Go to the gym", "weekly"
        )

        habits = self.service.list_habits()

        self.assertEqual(len(habits), 2)
        self.assertEqual(habits[0].task, "Read for 15 minutes")
        self.assertEqual(habits[1].task, "Go to the gym")


    def test_complete_habit(self):
        habit = self.service.create_habit(
            "Read for 15 minutes", "daily"
        )

        completion_time = datetime(
            2026, 11, 2, 10, 30, tzinfo=timezone.utc
        )

        completion_id = self.service.complete_habit(
            habit.id, completion_time
        )

        completions = self.repository.get_completions(habit.id)

        self.assertIsInstance(completion_id, int)
        self.assertEqual(len(completions), 1)
        self.assertEqual(completions[0], completion_time)


    def test_complete_nonexistent_habit(self):

        with self.assertRaises(ValueError):
            self.service.complete_habit(9999)


    def test_delete_habit(self):
        habit = self.service.create_habit(
            "Go to the gym", "weekly"
        )

        self.service.complete_habit(habit.id)

        deleted = self.service.delete_habit(habit.id)

        habits = self.service.list_habits()

        completions = self.repository.get_completions(habit.id)

        self.assertTrue(deleted)
        self.assertEqual(len(habits), 0)
        self.assertEqual(len(completions), 0)


    def test_delete_nonexistent_habit(self):

        deleted = self.service.delete_habit(9999)

        self.assertFalse(deleted)


    def test_filter_daily_habits(self):
        self.service.create_habit("Read for 15 minutes", "daily")
        self.service.create_habit("Go to the gym", "weekly")
        self.service.create_habit("Practise Python", "daily")

        daily_habits = self.service.filter_habits("daily")

        self.assertEqual(len(daily_habits), 2)
        self.assertEqual(daily_habits[0].task, "Read for 15 minutes")
        self.assertEqual(daily_habits[1].task, "Practise Python")


    def test_filter_invalid_periodicity(self):
        with self.assertRaises(ValueError):
            self.service.filter_habits("monthly")


    def test_service_longest_daily_streak(self):
        habit = self.service.create_habit(
            "Read for 15 minutes", "daily"
        )

        dates = [
            datetime(2026, 11, 2, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 3, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 4, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 6, 10, 0, tzinfo=timezone.utc)
        ]

        for completion_time in dates:
            self.service.complete_habit(habit.id, completion_time)

        result = self.service.longest_streak_for_habit(habit.id)

        self.assertEqual(result, 3)


    def test_service_longest_weekly_streak(self):
        habit = self.service.create_habit(
            "Go to the gym", "weekly"
        )

        dates = [
            datetime(2026, 11, 2, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 9, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 23, 10, 0, tzinfo=timezone.utc)
        ]

        for completion_time in dates:
            self.service.complete_habit(habit.id, completion_time)

        result = self.service.longest_streak_for_habit(habit.id)

        self.assertEqual(result, 2)


    def test_service_empty_streak(self):
        habit = self.service.create_habit(
            "Read for 15 minutes", "daily"
        )

        result = self.service.longest_streak_for_habit(habit.id)

        self.assertEqual(result, 0)


    def test_service_streak_nonexistent_habit(self):
        with self.assertRaises(ValueError):
            self.service.longest_streak_for_habit(9999)


    def test_service_overall_longest_streak(self):
        habit1 = self.service.create_habit(
            "Read for 15 minutes", "daily"
        )

        habit2 = self.service.create_habit(
            "Go to the gym", "weekly"
        )

        daily_dates = [
            datetime(2026, 11, 2, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 3, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 4, 10, 0, tzinfo=timezone.utc)
        ]

        weekly_dates = [
            datetime(2026, 11, 2, 12, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 9, 12, 0, tzinfo=timezone.utc)
        ]

        for completion_time in daily_dates:
            self.service.complete_habit(habit1.id, completion_time)

        for completion_time in weekly_dates:
            self.service.complete_habit(habit2.id, completion_time)

        result = self.service.longest_streak_all_habits()

        self.assertEqual(result, 3)


    def test_service_overall_empty_database(self):
        result = self.service.longest_streak_all_habits()

        self.assertEqual(result, 0)
    def test_service_berlin_daily_boundary(self):
        habit = self.service.create_habit(
            "Read for 15 minutes", "daily"
        )

        completions = [
            datetime(2026, 11, 2, 22, 30, tzinfo=timezone.utc),
            datetime(2026, 11, 2, 23, 30, tzinfo=timezone.utc)
        ]

        for completion_time in completions:
            self.service.complete_habit(habit.id, completion_time)

        result = self.service.longest_streak_for_habit(habit.id)

        self.assertEqual(result, 2)

import unittest

from habit_tracker.models import Habit


class TestHabit(unittest.TestCase):

    def test_create_daily_habit(self):
        habit = Habit("Read for 15 minutes", "daily")

        self.assertEqual(habit.task, "Read for 15 minutes")
        self.assertEqual(habit.periodicity, "daily")

    def test_create_weekly_habit(self):
        habit = Habit("Go to the gym", "weekly")

        self.assertEqual(habit.periodicity, "weekly")

    def test_empty_task(self):
        with self.assertRaises(ValueError):
            Habit("", "daily")

    def test_invalid_periodicity(self):
        with self.assertRaises(ValueError):
            Habit("Go swimming", "monthly")


if __name__ == "__main__":
    unittest.main()
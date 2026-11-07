import unittest
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from habit_tracker.analytics import (
    list_all_habits,
    filter_habits_by_periodicity,
    longest_daily_streak,
    longest_weekly_streak,
    longest_streak_overall
)


from habit_tracker.models import Habit


class TestAnalytics(unittest.TestCase):

    def setUp(self):
        self.habits = [
            Habit("Read for 15 minutes", "daily"),
            Habit("Go to the gym", "weekly"),
            Habit("Practise Python", "daily")
        ]


    def test_list_all_habits(self):
        result = list_all_habits(self.habits)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].task, "Read for 15 minutes")
        self.assertEqual(result[1].task, "Go to the gym")
        self.assertEqual(result[2].task, "Practise Python")
        self.assertIsNot(result, self.habits)


    def test_filter_daily_habits(self):
        result = filter_habits_by_periodicity(
            self.habits, "daily"
        )

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].task, "Read for 15 minutes")
        self.assertEqual(result[1].task, "Practise Python")


    def test_filter_weekly_habits(self):
        result = filter_habits_by_periodicity(
            self.habits, "weekly"
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].task, "Go to the gym")


    def test_invalid_periodicity(self):
        with self.assertRaises(ValueError):
            filter_habits_by_periodicity(
                self.habits, "monthly"
            )


    def test_empty_daily_streak(self):
        result = longest_daily_streak([], timezone.utc)

        self.assertEqual(result, 0)


    def test_three_consecutive_days(self):
        completions = [
            datetime(2026, 11, 2, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 3, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 4, 10, 0, tzinfo=timezone.utc)
        ]

        result = longest_daily_streak(completions, timezone.utc)

        self.assertEqual(result, 3)


    def test_broken_daily_streak(self):
        completions = [
            datetime(2026, 11, 2, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 3, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 4, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 6, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 7, 10, 0, tzinfo=timezone.utc)
        ]

        result = longest_daily_streak(completions, timezone.utc)

        self.assertEqual(result, 3)


    def test_duplicate_daily_completions(self):
        completions = [
            datetime(2026, 11, 2, 9, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 2, 18, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 3, 10, 0, tzinfo=timezone.utc)
        ]

        result = longest_daily_streak(completions, timezone.utc)

        self.assertEqual(result, 2)


    def test_daily_streak_local_timezone(self):
        local_timezone = timezone(timedelta(hours=2))

        completions = [
            datetime(2026, 11, 2, 22, 30, tzinfo=timezone.utc),
            datetime(2026, 11, 3, 22, 30, tzinfo=timezone.utc)
        ]

        result = longest_daily_streak(completions, local_timezone)

        self.assertEqual(result, 2)


    def test_empty_weekly_streak(self):
        result = longest_weekly_streak([], timezone.utc)

        self.assertEqual(result, 0)


    def test_three_consecutive_weeks(self):
        completions = [
            datetime(2026, 11, 2, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 11, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 16, 10, 0, tzinfo=timezone.utc)
        ]

        result = longest_weekly_streak(completions, timezone.utc)

        self.assertEqual(result, 3)


    def test_broken_weekly_streak(self):
        completions = [
            datetime(2026, 11, 2, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 9, 10, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 23, 10, 0, tzinfo=timezone.utc)
        ]

        result = longest_weekly_streak(completions, timezone.utc)

        self.assertEqual(result, 2)


    def test_duplicate_weekly_completions(self):
        completions = [
            datetime(2026, 11, 2, 9, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 8, 18, 0, tzinfo=timezone.utc),
            datetime(2026, 11, 9, 10, 0, tzinfo=timezone.utc)
        ]

        result = longest_weekly_streak(completions, timezone.utc)

        self.assertEqual(result, 2)


    def test_weekly_streak_across_year(self):
        completions = [
            datetime(2026, 12, 28, 10, 0, tzinfo=timezone.utc),
            datetime(2027, 1, 4, 10, 0, tzinfo=timezone.utc)
        ]

        result = longest_weekly_streak(completions, timezone.utc)

        self.assertEqual(result, 2)


    def test_weekly_streak_local_timezone(self):
        local_timezone = timezone(timedelta(hours=2))

        completions = [
            datetime(2026, 11, 1, 22, 30, tzinfo=timezone.utc),
            datetime(2026, 11, 8, 22, 30, tzinfo=timezone.utc)
        ]

        result = longest_weekly_streak(
            completions, local_timezone
        )

        self.assertEqual(result, 2)


    def test_overall_longest_streak(self):
        streak_lengths = [12, 3, 8, 4]

        result = longest_streak_overall(streak_lengths)

        self.assertEqual(result, 12)


    def test_overall_empty_streaks(self):
        result = longest_streak_overall([])

        self.assertEqual(result, 0)


    def test_overall_equal_streaks(self):
        streak_lengths = [5, 5, 3, 2]

        result = longest_streak_overall(streak_lengths)

        self.assertEqual(result, 5)


    def test_daily_streak_daylight_saving(self):
        berlin = ZoneInfo("Europe/Berlin")

        completions = [
            datetime(2026, 10, 25, 0, 30, tzinfo=timezone.utc),
            datetime(2026, 10, 25, 1, 30, tzinfo=timezone.utc)
        ]

        result = longest_daily_streak(completions, berlin)

        self.assertEqual(result, 1)


    def test_weekly_streak_berlin_boundary(self):
        berlin = ZoneInfo("Europe/Berlin")

        completions = [
            datetime(2026, 11, 1, 22, 30, tzinfo=timezone.utc),
            datetime(2026, 11, 1, 23, 30, tzinfo=timezone.utc)
        ]

        result = longest_weekly_streak(completions, berlin)

        self.assertEqual(result, 2)


    
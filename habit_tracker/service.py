from zoneinfo import ZoneInfo
LOCAL_TIMEZONE = ZoneInfo("Europe/Berlin")

from .models import Habit

from .analytics import (
    list_all_habits,
    filter_habits_by_periodicity,
    longest_daily_streak,
    longest_weekly_streak,
    longest_streak_overall
)




class HabitService:
    """Coordinate habit operations between the interface and repository."""

    def __init__(self, repository):
        self.repository = repository

    def create_habit(self, task, periodicity):
        """Create a new habit and save it to the database."""

        habit = Habit(task, periodicity)

        self.repository.save_habit(habit)

        return habit

    def list_habits(self):
        """Return all stored habits using the analytics module."""

        habits = self.repository.get_all_habits()

        return list_all_habits(habits)

    

    def complete_habit(self, habit_id, completed_at=None):
        """Record a completion for an existing habit."""

        habits = self.repository.get_all_habits()

        habit_exists = any(
            habit.id == habit_id for habit in habits
        )

        if not habit_exists:
            raise ValueError(f"Habit with ID {habit_id} does not exist.")

        return self.repository.add_completion(habit_id, completed_at)


    def delete_habit(self, habit_id):
        """Delete an existing habit and its completion history."""

        return self.repository.delete_habit(habit_id)


    def filter_habits(self, periodicity):
        """Return habits matching a daily or weekly period."""

        habits = self.repository.get_all_habits()

        return filter_habits_by_periodicity(habits, periodicity)


    def longest_streak_for_habit(self, habit_id, local_timezone=LOCAL_TIMEZONE):
        """Return the longest consecutive streak for a selected habit."""

        habits = self.repository.get_all_habits()

        habit = next(
            (item for item in habits if item.id == habit_id),
            None
        )

        if habit is None:
            raise ValueError(f"Habit with ID {habit_id} does not exist.")

        completions = self.repository.get_completions(habit_id)

        if habit.periodicity == "daily":
            return longest_daily_streak(completions, local_timezone)

        return longest_weekly_streak(completions, local_timezone)


    def longest_streak_all_habits(self, local_timezone=LOCAL_TIMEZONE):
        """Return the longest streak length among all stored habits."""

        habits = self.repository.get_all_habits()

        streak_lengths = [
            self.longest_streak_for_habit(habit.id, local_timezone)
            for habit in habits
        ]

        return longest_streak_overall(streak_lengths)
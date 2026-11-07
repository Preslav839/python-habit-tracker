import io
import tempfile
import unittest

from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import patch

from habit_tracker.cli import run_cli
from habit_tracker.repository import HabitRepository
from habit_tracker.service import HabitService


class TestHabitCLI(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        database_path = Path(self.temp_dir.name) / "test_cli.db"

        self.repository = HabitRepository(str(database_path))
        self.repository.initialize_database()

        self.service = HabitService(self.repository)


    def run_menu(self, answers):
        output = io.StringIO()

        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(output):
                run_cli(self.service)

        return output.getvalue()


    def test_exit_application(self):
        output = self.run_menu(["8"])

        self.assertIn(
            "Thank you for using Habit Tracker!",
            output
        )


    def test_create_habit_through_cli(self):
        output = self.run_menu([
            "1",
            "Read for 15 minutes",
            "daily",
            "8"
        ])

        habits = self.repository.get_all_habits()

        self.assertIn("Habit created successfully!", output)
        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0].task, "Read for 15 minutes")
        self.assertEqual(habits[0].periodicity, "daily")


    def test_view_habits_through_cli(self):
        self.service.create_habit(
            "Go to the gym", "weekly"
        )

        output = self.run_menu(["2", "8"])

        self.assertIn("YOUR HABITS", output)
        self.assertIn("Go to the gym", output)
        self.assertIn("weekly", output)


    def test_cancel_deletion(self):
        habit = self.service.create_habit(
            "Read for 15 minutes", "daily"
        )

        output = self.run_menu([
            "4",
            str(habit.id),
            "no",
            "8"
        ])

        habits = self.repository.get_all_habits()

        self.assertIn("Deletion cancelled.", output)
        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0].id, habit.id)


    def test_complete_habit_through_cli(self):
        habit = self.service.create_habit(
            "Read for 15 minutes", "daily"
        )

        output = self.run_menu([
            "3",
            str(habit.id),
            "8"
        ])

        completions = self.repository.get_completions(
            habit.id
        )

        self.assertIn(
            "Habit completed successfully!",
            output
        )

        self.assertEqual(len(completions), 1)


    def test_confirm_delete_habit_through_cli(self):
        habit = self.service.create_habit(
            "Temporary habit", "daily"
        )

        self.service.complete_habit(habit.id)

        output = self.run_menu([
            "4",
            str(habit.id),
            "yes",
            "8"
        ])

        remaining_habits = self.repository.get_all_habits()

        completions = self.repository.get_completions(
            habit.id
        )

        self.assertIn(
            "Habit deleted successfully!",
            output
        )

        self.assertEqual(len(remaining_habits), 0)
        self.assertEqual(len(completions), 0)


    def test_filter_habits_through_cli(self):
        self.service.create_habit(
            "Read for 15 minutes", "daily"
        )

        self.service.create_habit(
            "Go to the gym", "weekly"
        )

        self.service.create_habit(
            "Practise Python", "daily"
        )

        output = self.run_menu([
            "5",
            "daily",
            "8"
        ])

        self.assertIn("Read for 15 minutes", output)
        self.assertIn("Practise Python", output)
        self.assertNotIn("Go to the gym", output)


    def test_longest_streak_through_cli(self):
        habit = self.service.create_habit(
            "Read for 15 minutes", "daily"
        )

        self.service.complete_habit(habit.id)

        output = self.run_menu([
            "6",
            str(habit.id),
            "8"
        ])

        self.assertIn(
            "Habit: Read for 15 minutes",
            output
        )

        self.assertIn(
            "Longest streak: 1 day",
            output
        )


    def test_overall_streak_through_cli(self):
        habit1 = self.service.create_habit(
            "Read for 15 minutes", "daily"
        )

        self.service.create_habit(
            "Go to the gym", "weekly"
        )

        self.service.complete_habit(habit1.id)

        output = self.run_menu([
            "7",
            "8"
        ])

        self.assertIn(
            "Longest streak across all habits: 1",
            output
        )


    def test_invalid_menu_option(self):
        output = self.run_menu([
            "99",
            "8"
        ])

        self.assertIn(
            "Invalid option. Please try again.",
            output
        )

        self.assertIn(
            "Thank you for using Habit Tracker!",
            output
        )


    def test_empty_habit_description_cli(self):
        output = self.run_menu([
            "1",
            "",
            "daily",
            "8"
        ])

        habits = self.repository.get_all_habits()

        self.assertIn(
            "Task cannot be empty.",
            output
        )

        self.assertEqual(len(habits), 0)


    def test_invalid_periodicity_cli(self):
        output = self.run_menu([
            "1",
            "Go swimming",
            "monthly",
            "8"
        ])

        habits = self.repository.get_all_habits()

        self.assertIn(
            "Periodicity must be daily or weekly.",
            output
        )

        self.assertEqual(len(habits), 0)


    def test_non_numeric_habit_id_cli(self):
        habit = self.service.create_habit(
            "Read for 15 minutes", "daily"
        )

        output = self.run_menu([
            "3",
            "hello",
            "8"
        ])

        completions = self.repository.get_completions(
            habit.id
        )

        self.assertIn("Error:", output)

        self.assertEqual(len(completions), 0)


    def test_complete_nonexistent_habit_cli(self):
        output = self.run_menu([
            "3",
            "9999",
            "8"
        ])

        self.assertIn(
            "Habit with ID 9999 does not exist.",
            output
        )

        self.assertIn(
            "Thank you for using Habit Tracker!",
            output
        )


    def test_invalid_filter_periodicity_cli(self):
        output = self.run_menu([
            "5",
            "monthly",
            "8"
        ])

        self.assertIn(
            "Periodicity must be daily or weekly.",
            output
        )


    def test_analyse_nonexistent_habit_cli(self):
        output = self.run_menu([
            "6",
            "9999",
            "8"
        ])

        self.assertIn(
            "Habit with ID 9999 does not exist.",
            output
        )


    def test_overall_zero_periods_grammar(self):
        output = self.run_menu([
            "7",
            "8"
        ])

        self.assertIn(
            "Longest streak across all habits: 0 consecutive periods",
            output
        )


    def test_overall_one_period_grammar(self):
        habit = self.service.create_habit(
            "Read for 15 minutes", "daily"
        )

        self.service.complete_habit(habit.id)

        output = self.run_menu([
            "7",
            "8"
        ])

        self.assertIn(
            "Longest streak across all habits: 1 consecutive period\n",
            output
        )
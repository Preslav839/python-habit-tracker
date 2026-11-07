import sqlite3
from datetime import datetime, timezone
import unittest
import tempfile


from pathlib import Path

from habit_tracker.models import Habit
from habit_tracker.repository import HabitRepository


class TestHabitRepository(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        database_path = Path(self.temp_dir.name) / "test_habits.db"

        self.repository = HabitRepository(str(database_path))
        self.repository.initialize_database()

    
    def test_empty_database(self):
        habits = self.repository.get_all_habits()

        self.assertEqual(habits, [])

   
    def test_save_and_retrieve_habit(self):
        habit = Habit("Read for 15 minutes", "daily")

        habit_id = self.repository.save_habit(habit)

        habits = self.repository.get_all_habits()

        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0].id, habit_id)
        self.assertEqual(habits[0].task, "Read for 15 minutes")
        self.assertEqual(habits[0].periodicity, "daily")
        self.assertEqual(habits[0].created_at, habit.created_at)

    
    def test_database_persistence(self):
        habit = Habit("Go to the gym", "weekly")

        self.repository.save_habit(habit)

        new_repository = HabitRepository(
            self.repository.database_path
        )

        saved_habits = new_repository.get_all_habits()

        self.assertEqual(len(saved_habits), 1)
        self.assertEqual(saved_habits[0].task, "Go to the gym")
        self.assertEqual(saved_habits[0].periodicity, "weekly")



    def test_save_completion(self):
        habit = Habit("Read for 15 minutes", "daily")

        self.repository.save_habit(habit)

        completion_time = datetime(
            2026, 11, 2, 10, 30, tzinfo=timezone.utc
        )

        completion_id = self.repository.add_completion(
            habit.id, completion_time
        )

        completions = self.repository.get_completions(habit.id)

        self.assertIsInstance(completion_id, int)
        self.assertEqual(len(completions), 1)
        self.assertEqual(completions[0], completion_time)





    def test_multiple_completions(self):
        habit = Habit("Read for 15 minutes", "daily")

        self.repository.save_habit(habit)

        first_completion = datetime(
            2026, 11, 2, 10, 0, tzinfo=timezone.utc
        )

        second_completion = datetime(
            2026, 11, 3, 11, 0, tzinfo=timezone.utc
        )

        self.repository.add_completion(
            habit.id, second_completion
        )

        self.repository.add_completion(
            habit.id, first_completion
        )

        completions = self.repository.get_completions(habit.id)

        self.assertEqual(len(completions), 2)
        self.assertEqual(completions[0], first_completion)
        self.assertEqual(completions[1], second_completion)





    def test_completions_for_different_habits(self):
        habit1 = Habit("Read for 15 minutes", "daily")
        habit2 = Habit("Go to the gym", "weekly")

        self.repository.save_habit(habit1)
        self.repository.save_habit(habit2)

        completion_time = datetime(
            2026, 11, 2, 12, 0, tzinfo=timezone.utc
        )

        self.repository.add_completion(
            habit1.id, completion_time
        )

        habit1_completions = self.repository.get_completions(
            habit1.id
        )

        habit2_completions = self.repository.get_completions(
            habit2.id
        )

        self.assertEqual(len(habit1_completions), 1)
        self.assertEqual(len(habit2_completions), 0)




    def test_completion_invalid_habit(self):
        completion_time = datetime(
            2026, 11, 2, 12, 0, tzinfo=timezone.utc
        )

        with self.assertRaises(sqlite3.IntegrityError):
            self.repository.add_completion(
                9999, completion_time
            )


    def test_delete_habit_and_completions(self):
        habit1 = Habit("Read for 15 minutes", "daily")
        habit2 = Habit("Go to the gym", "weekly")

        self.repository.save_habit(habit1)
        self.repository.save_habit(habit2)

        self.repository.add_completion(habit1.id)
        self.repository.add_completion(habit1.id)
        self.repository.add_completion(habit2.id)

        deleted = self.repository.delete_habit(habit1.id)

        remaining_habits = self.repository.get_all_habits()

        habit1_completions = self.repository.get_completions(
            habit1.id
        )

        habit2_completions = self.repository.get_completions(
            habit2.id
        )

        self.assertTrue(deleted)
        self.assertEqual(len(remaining_habits), 1)
        self.assertEqual(remaining_habits[0].id, habit2.id)
        self.assertEqual(len(habit1_completions), 0)
        self.assertEqual(len(habit2_completions), 1)


    def test_delete_nonexistent_habit(self):
        deleted = self.repository.delete_habit(9999)

        self.assertFalse(deleted)

        habits = self.repository.get_all_habits()

        self.assertEqual(habits, [])
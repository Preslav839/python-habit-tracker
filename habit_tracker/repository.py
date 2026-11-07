import sqlite3
from datetime import datetime, timezone
from .models import Habit


class HabitRepository:
    """Manage storage of habits and completion records."""

    def __init__(self, database_path="habits.db"):
        self.database_path = database_path

    def initialize_database(self):
        """Create the database tables if they do not exist."""

        connection = sqlite3.connect(self.database_path)

        try:
            connection.execute("PRAGMA foreign_keys = ON")

            connection.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    periodicity TEXT NOT NULL
                        CHECK(periodicity IN ('daily', 'weekly')),
                    created_at TEXT NOT NULL
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completed_at TEXT NOT NULL,
                    FOREIGN KEY (habit_id)
                        REFERENCES habits(id)
                        ON DELETE CASCADE
                )
            """)

            connection.commit()

        finally:
            connection.close()





    def save_habit(self, habit):
        """Save a new habit to the database."""

        connection = sqlite3.connect(self.database_path)

        try:
            connection.execute("PRAGMA foreign_keys = ON")

            cursor = connection.execute("""
                INSERT INTO habits (task, periodicity, created_at)
                VALUES (?, ?, ?)
            """, (
                habit.task,
                habit.periodicity,
                habit.created_at.isoformat()
            ))

            connection.commit()

            habit.id = cursor.lastrowid

            return habit.id

        finally:
            connection.close()






    def get_all_habits(self):
       

        connection = sqlite3.connect(self.database_path)

        try:
            connection.execute("PRAGMA foreign_keys = ON")

            cursor = connection.execute("""
                SELECT id, task, periodicity, created_at
                FROM habits
                ORDER BY id
            """)

            rows = cursor.fetchall()

            habits = []

            for row in rows:
                habit = Habit(row[1], row[2])

                habit.id = row[0]
                habit.created_at = datetime.fromisoformat(row[3])

                habits.append(habit)

            return habits

        finally:
            connection.close()



    def get_completions(self, habit_id):
        """Retrieve completion timestamps for a specific habit."""

        connection = sqlite3.connect(self.database_path)

        try:
            cursor = connection.execute("""
                SELECT completed_at
                FROM completions
                WHERE habit_id = ?
                ORDER BY completed_at ASC
            """, (habit_id,))

            rows = cursor.fetchall()

            completions = []

            for row in rows:
                completed_at = datetime.fromisoformat(row[0])
                completions.append(completed_at)

            return completions

        finally:
            connection.close()


    def add_completion(self, habit_id, completed_at=None):
        """Record a completion for an existing habit."""

        if completed_at is None:
            completed_at = datetime.now(timezone.utc)

        if completed_at.tzinfo is None or completed_at.utcoffset() is None:
            raise ValueError("Completion time must include a timezone.")

        completed_at = completed_at.astimezone(timezone.utc)

        connection = sqlite3.connect(self.database_path)

        try:
            connection.execute("PRAGMA foreign_keys = ON")

            cursor = connection.execute("""
                INSERT INTO completions (habit_id, completed_at)
                VALUES (?, ?)
            """, (
                habit_id,
                completed_at.isoformat()
            ))

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()


    def delete_habit(self, habit_id):
        """Delete a habit and its associated completion records."""

        connection = sqlite3.connect(self.database_path)

        try:
            connection.execute("PRAGMA foreign_keys = ON")

            cursor = connection.execute("""
                DELETE FROM habits
                WHERE id = ?
            """, (habit_id,))

            connection.commit()

            return cursor.rowcount > 0

        finally:
            connection.close()
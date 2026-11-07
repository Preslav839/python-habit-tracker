from datetime import datetime, timezone


class Habit:
    """Represent a daily or weekly habit."""

    def __init__(self, task, periodicity):

        if not isinstance(task, str) or not task.strip():
            raise ValueError("Task cannot be empty.")

        if periodicity not in ("daily", "weekly"):
            raise ValueError("Periodicity must be daily or weekly.")

        self.id = None
        self.task = task.strip()
        self.periodicity = periodicity
        self.created_at = datetime.now(timezone.utc)
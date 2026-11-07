from datetime import timedelta

def list_all_habits(habits):
    """Return a new list containing all supplied habits."""

    return list(habits)


def filter_habits_by_periodicity(habits, periodicity):
    """Return habits matching the requested periodicity."""

    if periodicity not in ("daily", "weekly"):
        raise ValueError("Periodicity must be daily or weekly.")

    return list(
        filter(
            lambda habit: habit.periodicity == periodicity,
            habits
        )
    )


def longest_daily_streak(completions, local_timezone):
    """Calculate the longest streak of consecutive local calendar days."""

    completion_days = set()

    for completed_at in completions:
        if completed_at.tzinfo is None or completed_at.utcoffset() is None:
            raise ValueError("Completion timestamps must include a timezone.")

        local_day = completed_at.astimezone(local_timezone).date()
        completion_days.add(local_day)

    sorted_days = sorted(completion_days)

    longest_streak = 0
    current_streak = 0
    previous_day = None

    for day in sorted_days:

        if previous_day is not None and day == previous_day + timedelta(days=1):
            current_streak += 1

        else:
            current_streak = 1

        longest_streak = max(longest_streak, current_streak)

        previous_day = day

    return longest_streak


def longest_weekly_streak(completions, local_timezone):
    """Calculate the longest streak of consecutive Monday-to-Sunday weeks."""

    completion_weeks = set()

    for completed_at in completions:
        if completed_at.tzinfo is None or completed_at.utcoffset() is None:
            raise ValueError("Completion timestamps must include a timezone.")

        local_day = completed_at.astimezone(local_timezone).date()

        week_start = local_day - timedelta(days=local_day.weekday())

        completion_weeks.add(week_start)

    sorted_weeks = sorted(completion_weeks)

    longest_streak = 0
    current_streak = 0
    previous_week = None

    for week in sorted_weeks:

        if previous_week is not None and week == previous_week + timedelta(weeks=1):
            current_streak += 1

        else:
            current_streak = 1

        longest_streak = max(longest_streak, current_streak)

        previous_week = week

    return longest_streak


def longest_streak_overall(streak_lengths):
    """Return the maximum streak length across all habits."""

    return max(streak_lengths, default=0)
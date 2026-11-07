def run_cli(service):
    """Run the interactive habit tracker menu."""

    while True:
        print("\n================================")
        print("          HABIT TRACKER")
        print("================================")
        print("1. Create a habit")
        print("2. View all habits")
        print("3. Complete a habit")
        print("4. Delete a habit")
        print("5. Filter habits by periodicity")
        print("6. Longest streak for a habit")
        print("7. Longest streak across all habits")
        print("8. Exit")

        choice = input("\nChoose an option: ").strip()


        if choice == "1":
            print("\n===== CREATE A HABIT =====")

            task = input("Enter habit description: ")

            periodicity = input(
                "Enter periodicity (daily/weekly): "
            ).strip().lower()

            try:
                habit = service.create_habit(task, periodicity)

                print("\nHabit created successfully!")
                print("Habit ID:", habit.id)
                print("Task:", habit.task)
                print("Periodicity:", habit.periodicity)

            except ValueError as error:
                print("\nError:", error)


        elif choice == "2":
            print("\n===== YOUR HABITS =====")

            habits = service.list_habits()

            if not habits:
                print("No habits found.")

            else:
                for habit in habits:
                    print("-------------------------")
                    print("ID:", habit.id)
                    print("Task:", habit.task)
                    print("Periodicity:", habit.periodicity)
                    print("Created:", habit.created_at)


        elif choice == "3":
            print("\n===== COMPLETE A HABIT =====")

            try:
                habit_id = int(input("Enter habit ID: ").strip())

                if habit_id <= 0:
                    raise ValueError("Habit ID must be a positive number.")

                completion_id = service.complete_habit(habit_id)

                print("\nHabit completed successfully!")
                print("Completion ID:", completion_id)

            except ValueError as error:
                print("\nError:", error)


        elif choice == "4":
            print("\n===== DELETE A HABIT =====")

            try:
                habit_id = int(input("Enter habit ID: ").strip())

                if habit_id <= 0:
                    raise ValueError("Habit ID must be a positive number.")

                confirmation = input(
                    "Are you sure you want to delete this habit? (yes/no): "
                ).strip().lower()

                if confirmation == "yes":
                    deleted = service.delete_habit(habit_id)

                    if deleted:
                        print("\nHabit deleted successfully!")
                    else:
                        print("\nHabit not found.")

                else:
                    print("\nDeletion cancelled.")

            except ValueError as error:
                print("\nError:", error)


        elif choice == "5":
            print("\n===== FILTER HABITS =====")

            periodicity = input(
                "Enter periodicity (daily/weekly): "
            ).strip().lower()

            try:
                habits = service.filter_habits(periodicity)

                if not habits:
                    print("\nNo matching habits found.")

                else:
                    print("\n===== MATCHING HABITS =====")

                    for habit in habits:
                        print("-------------------------")
                        print("ID:", habit.id)
                        print("Task:", habit.task)
                        print("Periodicity:", habit.periodicity)

            except ValueError as error:
                print("\nError:", error)


        elif choice == "6":
            print("\n===== HABIT STREAK ANALYSIS =====")

            try:
                habit_id = int(input("Enter habit ID: ").strip())

                if habit_id <= 0:
                    raise ValueError("Habit ID must be positive.")

                streak = service.longest_streak_for_habit(habit_id)

                habits = service.list_habits()

                habit = next(
                    (item for item in habits if item.id == habit_id),
                    None
                )

                if habit.periodicity == "daily":
                    unit = "day"
                else:
                    unit = "week"

                if streak != 1:
                    unit += "s"

                print("\n===== ANALYSIS RESULT =====")
                print("Habit:", habit.task)
                print("Periodicity:", habit.periodicity)
                print("Longest streak:", streak, unit)

            except ValueError as error:
                print("\nError:", error)


        elif choice == "7":
            print("\n===== OVERALL HABIT ANALYSIS =====")

            longest = service.longest_streak_all_habits()

            unit = "period" if longest == 1 else "periods"

            print(
                f"\nLongest streak across all habits: "
                f"{longest} consecutive {unit}"
            )

            print("Daily habits use days.")
            print("Weekly habits use weeks.")

        elif choice == "8":
            print("\nThank you for using Habit Tracker!")
            break

        else:
            print("\nInvalid option. Please try again.")
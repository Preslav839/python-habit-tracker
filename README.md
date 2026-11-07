# Habit Tracker

## 1. Project Overview

Habit Tracker is a Python application that helps users manage their daily and weekly habits. The main purpose of the application is to make it easier to keep track of regular activities and see how consistently they have been completed.

Users can create habits, mark them as completed, and check their progress through streak calculations. The application runs in the terminal and stores information in an SQLite database. This means that habits and their completion histories remain saved after the application is closed.

I developed this project as part of the Object Oriented and Functional Programming with Python course at IU International University of Applied Sciences.

The project combines object-oriented and functional programming. Object-oriented programming is used to organise the application into different classes, while functional programming is mainly used to analyse completion records and calculate streaks.

## 2. Features

The Habit Tracker allows users to create habits and choose whether they should be completed daily or weekly. Each habit has its own description, periodicity, and ID, which makes it possible to manage different habits separately.

Users can view all their saved habits, record completions, and delete habits they no longer want to track. Before a habit is deleted, the application asks for confirmation to prevent accidental deletion.

The application also allows users to filter habits by periodicity. For example, users can display only their daily habits or only their weekly habits.

Another important feature is the calculation of habit streaks. The application can calculate the longest streak for an individual habit and find the highest streak count across all saved habits. Daily streaks are based on consecutive calendar days, while weekly streaks are based on consecutive calendar weeks.

All habit information and completion records are stored in an SQLite database. This allows the application to keep a completion history and use it for later calculations.

The project also includes a demonstration mode with five predefined habits and four weeks of example completion data. This makes it possible to explore the features without having to create several weeks of records manually.

To make the application more reliable, I added input validation and automated tests. If a user enters incorrect information, such as an invalid habit ID or an unsupported periodicity, the application displays an error message and allows the user to continue.

## 3. System Requirements

The application was developed and tested on Windows using Python 3.14.4.

SQLite is used to store habits and completion records. Since SQLite is included in Python's standard library, a separate database server is not required.

The project also uses Python's built-in `unittest` framework for automated testing.

The only additional Python dependency is `tzdata`, which provides timezone information. The application uses the `Europe/Berlin` timezone when calculating streaks so that completions are assigned to the correct local day or week.

The Habit Tracker runs directly in a terminal and does not require a graphical user interface.

## 4. Installation

### Downloading the Project

First, download the project from its GitHub repository and extract it into a folder on your computer.

Open the project folder in Visual Studio Code or another code editor. Then open a terminal in the main project folder, where the `main.py` file is located.

### Installing the Required Dependency

Before starting the application, install the required Python dependency.

On Windows, using Python 3.14, run:

```powershell
py -3.14 -m pip install -r requirements.txt
```

This command installs the packages listed in `requirements.txt`, including the timezone dependency used by the application.

### Starting the Application

Once the dependency has been installed, start the Habit Tracker by entering:

```powershell
py -3.14 main.py
```

The application menu will appear in the terminal.

The program uses an SQLite database called `habits.db` to store the user's information. If this database does not already exist, it is created automatically when the application starts.

The commands above are written for Windows with Python 3.14. On other operating systems, the corresponding `python` or `python3` command can be used with a compatible Python installation.

## 5. Usage

The Habit Tracker is controlled through a menu in the terminal. When the application starts, users can choose between eight options by entering the corresponding number.

### Creating and Managing Habits

To create a new habit, select option `1`. The application asks for a description and whether the habit should be completed daily or weekly.

For example, a user could create a habit called "Read for 15 minutes" and choose "daily" as its periodicity. The application then saves the habit in the database and assigns it an ID.

Option `2` displays all saved habits, including their IDs, descriptions, and periodicities. This allows users to see which habits they are currently tracking.

If a user no longer wants to track a habit, they can select option `4` and enter the habit ID. Before deleting the habit, the application asks for confirmation. If the user confirms, the habit and its completion records are removed from the database. If the user cancels, the habit remains unchanged.

### Recording Habit Completions

To mark a habit as completed, select option `3` and enter its ID.

The application records the completion time and saves it in the database. Each completion becomes part of the habit's history and can be used later when calculating streaks.

Users can record multiple completions for the same habit. However, multiple completions during the same day or week count as one completed period when calculating streaks.

### Filtering and Analysing Habits

Option `5` allows users to filter their habits by periodicity. By entering "daily" or "weekly", users can display only the habits that match their selection.

Option `6` calculates the longest streak for a selected habit. After entering the habit ID, the application checks its completion history and finds the longest sequence of consecutive completed days or weeks.

For example, if a daily habit was completed on five consecutive days, its longest streak would be five days. If a weekly habit was completed during four consecutive weeks, its longest streak would be four weeks.

Option `7` calculates the highest streak count across all saved habits. The application compares the longest streaks of the individual habits and displays the highest number of consecutive periods.

### How Streaks Are Calculated

The application uses the recorded completion timestamps to calculate streaks.

For daily habits, a streak increases when the habit is completed on consecutive calendar days. For weekly habits, a streak increases when the habit is completed during consecutive calendar weeks.

If a day or week is missed, the streak is interrupted. The application checks the entire available completion history to find the longest streak, rather than only looking at the most recent completions.

Completion timestamps are stored in UTC and converted to the `Europe/Berlin` timezone when calculating daily and weekly streaks. This helps ensure that completions close to midnight are assigned to the correct local date.

### Exiting the Application

To close the Habit Tracker, select option `8`.

The application closes, but all saved habits and completion records remain in the database. They will still be available the next time the program is started.

The application also handles interruptions such as pressing `Ctrl + C`, allowing it to close without displaying an unnecessary error message.

## 6. Demonstration Mode

The Habit Tracker includes a demonstration mode that allows users to explore the application without having to create their own habits or record several weeks of activity.

The demonstration database contains five predefined habits. Three of them are daily habits: "Read for 15 minutes", "Stretch", and "Practise Python". The other two are weekly habits: "Plan week" and "Call friend".

These habits include completion records covering four weeks. Some habits were completed more consistently than others, which makes it possible to demonstrate different streak lengths.

### Starting Demonstration Mode

To start the application in demonstration mode, open a terminal in the main project folder and enter:

```powershell
py -3.14 main.py --demo
```

The application loads the five predefined habits together with their completion histories.

Users can then explore the menu, view the saved habits, record completions, filter habits, and calculate streaks using the example data.

Demonstration mode uses a temporary copy of the original demonstration database. This means that changes made while exploring the application do not permanently affect the predefined data. The original database remains available for future demonstrations.

### Generating the Demonstration Data

If the demonstration database is missing, it can be generated by running:

```powershell
py -3.14 seed_demo.py
```

The script creates the example database with the five predefined habits and their completion histories.

This makes it possible to prepare the demonstration data again when setting up the project.

## 7. Running Tests

The project uses Python's built-in `unittest` framework to check whether the different parts of the application work correctly.

Automated testing was used throughout development to identify errors and verify that new features did not affect the existing functionality.

The tests cover habit creation and validation, database operations, completion tracking, habit deletion, and streak calculations.

They also check the command-line interface, filtering, invalid user input, timezone handling, demonstration data, and application startup.

### Executing the Tests

To run the complete test suite, open a terminal in the main project folder and enter:

```powershell
py -3.14 -m unittest discover -s tests -v
```

This command runs all test files inside the `tests` folder and displays their results in the terminal.

At this stage of development, the project contains **76 automated tests**, and all 76 passed successfully during the latest test run.

For tests that involve saving or deleting information, temporary databases are used where appropriate. This prevents the automated tests from changing the user's normal habit data.

## 8. Project Structure

The Habit Tracker is organised into separate Python files. Each file has a specific responsibility, which makes the code easier to understand, test, and maintain.

### Habit Model and Database

The main application code is stored inside the `habit_tracker` folder.

The `models.py` file contains the `Habit` class. This class represents an individual habit and checks whether the description and periodicity are valid.

The `repository.py` file handles communication with the SQLite database. It is responsible for saving habits, retrieving stored information, recording completions, and deleting records.

The database contains separate tables for habits and their completion records. Each completion is linked to its corresponding habit.

### Application Logic and Analytics

The `service.py` file connects the different parts of the application. It handles operations such as creating, completing, and deleting habits. It also calls the analytics functions when users request streak calculations.

The `analytics.py` file contains the functions used to filter habits and calculate daily and weekly streaks.

These functions receive the required information, process it, and return the result without changing the original completion records. This is where functional programming is mainly used in the project.

### Command-Line Interface

The `cli.py` file contains the command-line interface. It displays the menu, receives user input, and communicates with the service layer.

The `main.py` file is located in the main project folder and is responsible for starting the application. It also allows users to choose between normal mode and demonstration mode.

### Demonstration Data

The `seed_demo.py` file generates the five predefined habits and the four weeks of example completion data used in demonstration mode.

The `demo_habits.db` file stores this predefined information.

The application also uses a separate database called `habits.db` for normal use. This database contains the user's own habits and completion histories.

### Automated Tests and Dependencies

The `tests` folder contains the automated tests for the different parts of the application.

The tests are separated into different files based on the components they check. These include the habit model, database operations, service layer, analytics, demonstration data, command-line interface, and application startup.

The `requirements.txt` file lists the external Python dependency needed to run the application.

The `README.md` file contains the installation instructions, usage explanations, and information about the project structure.

Overall, the project follows a structure that separates the user interface, application logic, database operations, and analytics. This makes it easier to test individual components and make changes without affecting the entire application.
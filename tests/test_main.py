import io
import tempfile
import unittest

from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import patch

from main import main, start_tracker


class TestApplicationStartup(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.database_path = (
            Path(self.temp_dir.name) / "startup_test.db"
        )


    def test_keyboard_interrupt_closes_cleanly(self):
        output = io.StringIO()

        with patch("main.run_cli", side_effect=KeyboardInterrupt):
            with redirect_stdout(output):
                start_tracker(self.database_path)

        self.assertIn(
            "Habit Tracker closed.",
            output.getvalue()
        )


    def test_end_of_input_closes_cleanly(self):
        output = io.StringIO()

        with patch("main.run_cli", side_effect=EOFError):
            with redirect_stdout(output):
                start_tracker(self.database_path)

        self.assertIn(
            "Habit Tracker closed.",
            output.getvalue()
        )


    def test_normal_mode_uses_main_database(self):
        with patch("main.BASE_DIR", Path(self.temp_dir.name)):
            with patch("sys.argv", ["main.py"]):
                with patch("main.start_tracker") as mocked_start:
                    main()

        expected_path = Path(self.temp_dir.name) / "habits.db"

        mocked_start.assert_called_once_with(expected_path)


    def test_demo_mode_missing_database(self):
        output = io.StringIO()

        with patch("main.BASE_DIR", Path(self.temp_dir.name)):
            with patch("sys.argv", ["main.py", "--demo"]):
                with patch("main.start_tracker") as mocked_start:
                    with redirect_stdout(output):
                        main()

        mocked_start.assert_not_called()

        self.assertIn(
            "Demonstration database not found.",
            output.getvalue()
        )


    def test_demo_mode_uses_temporary_copy(self):
        original_database = (
            Path(self.temp_dir.name) / "demo_habits.db"
        )

        original_database.write_bytes(b"test database content")

        temporary_paths = []

        def check_temporary_database(database_path):
            temporary_path = Path(database_path)

            self.assertTrue(temporary_path.exists())

            self.assertNotEqual(
                temporary_path,
                original_database
            )

            self.assertEqual(
                temporary_path.read_bytes(),
                original_database.read_bytes()
            )

            temporary_paths.append(temporary_path)

        with patch("main.BASE_DIR", Path(self.temp_dir.name)):
            with patch("sys.argv", ["main.py", "--demo"]):
                with patch(
                    "main.start_tracker",
                    side_effect=check_temporary_database
                ):
                    with redirect_stdout(io.StringIO()):
                        main()

        self.assertTrue(original_database.exists())

        self.assertFalse(temporary_paths[0].exists())

        self.assertEqual(
            original_database.read_bytes(),
            b"test database content"
        )
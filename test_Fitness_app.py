import unittest
import tkinter as tk
from tkinter import messagebox
from unittest.mock import patch
from ACEest_Fitness  import FitnessTrackerApp  # Replace 'your_module' with the actual module name

class TestFitnessTrackerApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window during tests
        self.app = FitnessTrackerApp(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('tkinter.messagebox.showerror')
    def test_add_workout_empty_fields(self, mock_error):
        self.app.workout_entry.insert(0, "")
        self.app.duration_entry.insert(0, "")
        self.app.add_workout()
        mock_error.assert_called_once_with("Error", "Please enter both workout and duration.")

    @patch('tkinter.messagebox.showerror')
    def test_add_workout_invalid_duration(self, mock_error):
        self.app.workout_entry.insert(0, "Running")
        self.app.duration_entry.insert(0, "abc")
        self.app.add_workout()
        mock_error.assert_called_once_with("Error", "Duration must be a number.")

    @patch('tkinter.messagebox.showinfo')
    def test_add_workout_valid_input(self, mock_info):
        self.app.workout_entry.insert(0, "Running")
        self.app.duration_entry.insert(0, "30")
        self.app.add_workout()
        mock_info.assert_called_once_with("Success", "'Running' added successfully!")
        self.assertEqual(len(self.app.workouts), 1)
        self.assertEqual(self.app.workouts[0], {"workout": "Running", "duration": 30})

    @patch('tkinter.messagebox.showinfo')
    def test_view_workouts_empty(self, mock_info):
        self.app.view_workouts()
        mock_info.assert_called_once_with("Workouts", "No workouts logged yet.")

    @patch('tkinter.messagebox.showinfo')
    def test_view_workouts_with_entries(self, mock_info):
        self.app.workouts = [
            {"workout": "Running", "duration": 30},
            {"workout": "Cycling", "duration": 45}
        ]
        self.app.view_workouts()
        expected_output = "Logged Workouts:\n1. Running - 30 minutes\n2. Cycling - 45 minutes\n"
        mock_info.assert_called_once_with("Workouts", expected_output)

if __name__ == "__main__":
    unittest.main()
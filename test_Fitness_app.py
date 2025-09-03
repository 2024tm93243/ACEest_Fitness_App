import pytest
from unittest.mock import MagicMock, patch
import tkinter as tk
from fitness_tracker_app import FitnessTrackerApp

@pytest.fixture
def app():
    with patch("tkinter.Tk") as MockTk:
        root = MockTk()
        root.title = MagicMock()
        app_instance = FitnessTrackerApp(root)
        app_instance.workout_entry = MagicMock()
        app_instance.duration_entry = MagicMock()
        yield app_instance

def test_add_valid_workout(app):
    app.workout_entry.get.return_value = "Running"
    app.duration_entry.get.return_value = "30"
    with patch("tkinter.messagebox.showinfo") as mock_info:
        app.add_workout()
        assert len(app.workouts) == 1
        assert app.workouts[0]["workout"] == "Running"
        assert app.workouts[0]["duration"] == 30
        mock_info.assert_called_once()

def test_add_workout_missing_fields(app):
    app.workout_entry.get.return_value = ""
    app.duration_entry.get.return_value = ""
    with patch("tkinter.messagebox.showerror") as mock_error:
        app.add_workout()
        assert len(app.workouts) == 0
        mock_error.assert_called_once()

def test_add_workout_invalid_duration(app):
    app.workout_entry.get.return_value = "Cycling"
    app.duration_entry.get.return_value = "abc"
    with patch("tkinter.messagebox.showerror") as mock_error:
        app.add_workout()
        assert len(app.workouts) == 0
        mock_error.assert_called_once()

def test_view_workouts_empty(app):
    with patch("tkinter.messagebox.showinfo") as mock_info:
        app.view_workouts()
        mock_info.assert_called_once_with("Workouts", "No workouts logged yet.")

def test_view_workouts_with_entries(app):
    app.workouts.append({"workout": "Swimming", "duration": 45})
    with patch("tkinter.messagebox.showinfo") as mock_info:
        app.view_workouts()
        assert mock_info.call_count == 1
        args = mock_info.call_args[0][1]
        assert "Swimming" in args
        assert "45 minutes" in args
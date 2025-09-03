import pytest
import tkinter as tk
from tkinter import messagebox
from unittest.mock import patch
from fitness_tracker_app import FitnessTrackerApp

@pytest.fixture
def app():
    root = tk.Tk()
    app_instance = FitnessTrackerApp(root)
    yield app_instance
    root.destroy()

def test_add_valid_workout(app):
    app.workout_entry.insert(0, "Running")
    app.duration_entry.insert(0, "30")
    with patch.object(messagebox, 'showinfo') as mock_info:
        app.add_workout()
        assert len(app.workouts) == 1
        assert app.workouts[0]["workout"] == "Running"
        assert app.workouts[0]["duration"] == 30
        mock_info.assert_called_once()

def test_add_workout_missing_fields(app):
    app.workout_entry.insert(0, "")
    app.duration_entry.insert(0, "")
    with patch.object(messagebox, 'showerror') as mock_error:
        app.add_workout()
        assert len(app.workouts) == 0
        mock_error.assert_called_once()

def test_add_workout_invalid_duration(app):
    app.workout_entry.insert(0, "Cycling")
    app.duration_entry.insert(0, "abc")
    with patch.object(messagebox, 'showerror') as mock_error:
        app.add_workout()
        assert len(app.workouts) == 0
        mock_error.assert_called_once()

def test_view_workouts_empty(app):
    with patch.object(messagebox, 'showinfo') as mock_info:
        app.view_workouts()
        mock_info.assert_called_once_with("Workouts", "No workouts logged yet.")

def test_view_workouts_with_entries(app):
    app.workouts.append({"workout": "Swimming", "duration": 45})
    with patch.object(messagebox, 'showinfo') as mock_info:
        app.view_workouts()
        assert mock_info.call_count == 1
        args = mock_info.call_args[0][1]
        assert "Swimming" in args
        assert "45 minutes" in args

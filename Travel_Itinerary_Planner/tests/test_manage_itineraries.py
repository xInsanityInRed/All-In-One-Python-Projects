import unittest
from src.manage_itineraries import add_itinerary, edit_itinerary, add_new_flight, add_new_attraction, view_itineraries, delete_itinerary, delete_itinerary_item, print_table
from src.file_handler import load_itineraries, save_itineraries

import os
import io
from rich.console import Console
from rich.table import Table

from pick import Picker

TEST_FILE = "test_itineraries.bin"

"""
Tests all of the functions in manage_itineraries.py

"""


class TestManageItineraries(unittest.TestCase):
    """
    Unit tests for manage_itineraries.py functionalities including adding, editing, viewing, deleting, filtering,
    and persisting itineraries to and from a binary file.
    """

    def setUp(self):
        """
        Set up the test environment by initialising an empty task list
        and backing up the original itinerary binary file.
        """
        self.itineraries = []
        self.original_file = "itineraries.bin"
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)
        os.rename("itineraries.bin", TEST_FILE) if os.path.exists("itineraries.bin") else None

    def tearDown(self):
        """
        Clean up the test environment by removing any test-created binary files
        and restoring the original task binary file.
        """
        if os.path.exists("itineraries.bin"):
            os.remove("itineraries.bin")
        os.rename(TEST_FILE, "itineraries.bin") if os.path.exists(TEST_FILE) else None

    def test_add_itinerary(self):
        """
        Test adding a new task to the task list.
        Verify that the task is successfully added and the list size increases.
        """
        test_itinerary = [{
            "name": "trip", "location": "Japan", "description": "description", "start_date": "12-12-2026", "end_date": "28-01-2027", "flights": [{
                "flight name": "Perth to Narita",
                "departure airport": "Perth",
                "departure date": "12-12-2026 08:00",
                "arrival airport": "Narita",
                "arrival date": "12-12-2026 16:00"
            },
                {
                    "flight name": "Narita to Perth",
                    "departure airport": "Narita",
                    "departure date": "27-01-2027 23:00",
                    "arrival airport": "Perth",
                    "arrival date": "28-01-2027 07:00"
                }
            ],
            "attractions": [{
                "attraction name": "Hike",
                "address": "123 Hike Lane",
                "summary": "A cool hike with good views",
                "tag(s)": "outdoors"
            },
                {
                    "attraction name": "Dinner spot",
                    "address": "49 Sweet Cove",
                    "summary": "A lovely dinner spot",
                    "tag(s)": "dinner, romantic"
                }
            ]}]
        
        result = add_itinerary(self.itineraries, name=test_itinerary["name"], location=test_itinerary["location"], description=test_itinerary["description"], start_date=test_itinerary["start_date"], end_date=test_itinerary["end_date"], flights=test_itinerary["flights"], attractions=test_itinerary["attractions"])

        print(self.itineraries)
        self.assertTrue(result)
        self.assertEqual(len(self.itineraries), 1)

    def test_add_duplicate_itinerary(self):
        """
        Test adding a duplicate task with the same title.
        Verify that duplicates are not allowed and the function returns False.
        """
        test_itinerary = [{
            "name": "trip", "location": "Japan", "description": "description", "start_date": "12-12-2026", "end_date": "28-01-2027", "flights": [{
                "flight name": "Perth to Narita",
                "departure airport": "Perth",
                "departure date": "12-12-2026 08:00",
                "arrival airport": "Narita",
                "arrival date": "12-12-2026 16:00"
            },
                {
                    "flight name": "Narita to Perth",
                    "departure airport": "Narita",
                    "departure date": "27-01-2027 23:00",
                    "arrival airport": "Perth",
                    "arrival date": "28-01-2027 07:00"
                }
            ],
            "attractions": [{
                "attraction name": "Hike",
                "address": "123 Hike Lane",
                "summary": "A cool hike with good views",
                "tag(s)": "outdoors"
            },
                {
                    "attraction name": "Dinner spot",
                    "address": "49 Sweet Cove",
                    "summary": "A lovely dinner spot",
                    "tag(s)": "dinner, romantic"
                }
            ]}]

        add_itinerary(self.itineraries, "Test Task", "Description", "01-12-2021", "Pending")
        result = add_itinerary(self.itineraries, "Test Task", "New Description", "02-12-2024", "Pending")
        self.assertFalse(result)

    def test_add_invalid_itinerary(self):
        """
        Test adding a task with an invalid due date format.
        Verify that the function handles invalid input gracefully and returns False.
        """
        result = add_itinerary(self.itineraries, "Test Task", "Description", "2024-12-01", "Pending")
        self.assertFalse(result)

    def test_delete_itinerary(self):
        """
        Test deleting a task by its title.
        Verify that the task is removed from the list and the list size decreases.
        """
        add_itinerary(self.itineraries, "Task to Delete", "Description", "01-12-2024", "Pending")
        result = delete_itinerary(self.itineraries, "Task to Delete")
        self.assertTrue(result)
        self.assertEqual(len(self.itineraries), 0)

    def test_view_itineraries(self):
        """
        Docstring for test_view_itineraries
        
        
        """
        pass

    def test_save_and_load_itineraries(self):
        """
        Test saving itineraries to a file and loading them back.
        Verify that the saved itineraries are correctly loaded with the same data.
        """
        add_itinerary(self.itineraries, "Persistent Task", "Description", "01-12-2024", "Pending")
        save_itineraries(self.itineraries)
        loaded_itineraries = load_itineraries()
        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0].title, "Persistent Task")

    def test_rich_builtin_table(self):
        """
        Test saves itineraries to the task list and displays new formatted table using "rich" Table component.
        Verify that the terminal's output matches the itineraries saved in the list of itineraries.

        Documentation for capturing output made by rich: https://rich.readthedocs.io/en/latest/console.html#capturing-output
        Extra resources:
        - [QUESTION] How to test output of rich.Table? #247 https://github.com/Textualize/rich/issues/247
        """

        #Test view_itineraries function to verify itineraries are saved
        test_table = Table(title="Test List")
        test_table.add_column("Task", justify="center")
        test_table.add_column("Description", justify="center")
        test_table.add_column("Due Date", justify="center", no_wrap=True)
        test_table.add_column("Status", justify="left", no_wrap=True)
        add_itinerary(self.itineraries, "Test Task", "N/A", "01-12-2024", "Pending")

        save_itineraries(self.itineraries)
        view_itineraries(self.itineraries)

        #Test that the output printed in the terminal has the same format as the rich component's "Table" class
        test_console = Console(file=io.StringIO())
        test_console.print(test_table)
        test_output = test_console.file.getvalue()
        print(test_output)

        self.assertIs(type(test_table), type(Table()))
        self.assertIs(type(test_output), str)

    def test_pick_move_up_down_function(self):
        """
        Test creates a variety of itinerary options and asserts that the current option highlighted (*not* entered) matches the picker's position in the "options" list.
        Verifies moving up and down the list in a "Picker" screen works.
        Documentation for capturing output made by pick: https://github.com/aisk/pick/blob/master/tests/test_pick.py
        """
        title = "Please choose an itinerary: "
        options = ["TBA", "this_itinerary", "that_itinerary"]
        itinerary_picker = Picker(options, title)
        assert itinerary_picker.get_selected() == ("TBA", 0)
        itinerary_picker.move_up()
        assert itinerary_picker.get_selected() == ("that_itinerary", 2)
        itinerary_picker.move_down()
        itinerary_picker.move_down()
        assert itinerary_picker.get_selected() == ("this_itinerary", 1)

    def test_pick_filter_tasks_by_status(self):
        """
        Test the "pick" library's ability to correctly filter tasks based on their status (e.g., 'completed').
        Verify that only tasks matching the specified status are returned.
        """
        task1 = Task("Task 1", "Desc", "01-12-2024", "pending")
        task2 = Task("Task 2", "Desc", "02-12-2024", "complete")
        self.tasks.extend([task1, task2])
        save_tasks(self.tasks)
        task_filter_title = "Please choose a task: "
        status_options = ["TBA", "pending", "complete"]
        task_picker = Picker(status_options, task_filter_title, default_index=2)
        assert task_picker.get_selected() == ("complete", 2)

        filter_option = status_options[task_picker.default_index]
        print("Filter option selected:", filter_option)

        pick_filter = filter_tasks_by_status(self.tasks, filter_option)
        self.assertEqual(pick_filter[0].title, "Task 2")


if __name__ == "__main__":
    unittest.main()



pass

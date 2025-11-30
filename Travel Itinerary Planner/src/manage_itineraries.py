from src.file_handler import load_itineraries, save_itineraries
from datetime import datetime
from pick import pick
from anytree import Node, RenderTree
from pickpack import pickpack
from rich.console import Console
from rich.table import Table
from rich import print
"""
This file contains all of the functions needed for the Travel Itinerary Planner.
It allows the user to add, edit, view, delete, and export an itinerary while checking for errors in input.
"""


def add_itinerary(itinerary_list, name, location, summary, start_date, end_date, flights, attractions):
    '''
    Docstring for add_itinerary

    Returns:
        bool: True if Itinerary is added without issue, otherwise False.

    Side Effects:
        - Saves the updated itinerary list to a file using `save_itineraries`.
    '''
    # TEST: check that all items have been transferred correctly
    print(name)
    print(location)
    print(summary)
    print(start_date)
    print(end_date)
    print(flights.items())
    print(attractions.items())

    if validate_dates(start_date, end_date, flights):
        # Add the new itinerary after validation checks
        new_itinerary = {
            "name": name,
            "location": location,
            "summary": summary,
            "start_date": start_date,
            "end_date": end_date,
            "flights": flights,
            "attractions": attractions
        }
        print(new_itinerary)

        itinerary_list.append(new_itinerary)
        print(itinerary_list)

        save_itineraries(itinerary_list)
        return True
    else:
        return False


def edit_itinerary(chosen_itinerary):
    # Use pickpack module (https://github.com/anafvana/pickpack#map-function-for-nested-lists)
    pass


def view_itineraries(itinerary_list):
    # Use pick module: Ask if they would like to view all itineraries, or a specific one
    view_prompt = 'Would you like to view all the existing itineraries?:  '
    view_options = ['View All', 'View One']
    option, index = pick(view_options, view_prompt)
    if option == 'View All':
        print(f"\nFilter selected: {option}")
        # Use rich to print table
        print_table(itinerary_list)
    elif option == 'View One':
        # Use pick module to select an itinerary by name and location
        print(f"\nFilter selected: {option}")
        itinerary_choice = 'Which itinerary would you like to view?: '
        itinerary_options = []

        for trip in itinerary_list:
            itinerary_options.append(trip["name"])
        filter_option, filter_index = pick(itinerary_options, itinerary_choice)

        # Filter itinerary list
        filtered_itineraries = []
        for itinerary in itinerary_list:
            if filter_option == itinerary["name"]:
                filtered_itineraries.append(itinerary)
        # Use rich to print table
        print_table(filtered_itineraries)
    else:
        print("Error: Valid filter not selected, returning to Task Manager menu.\n")
        return False
    return True


def delete_itinerary(chosen_itinerary):
    itinerary_list = load_itineraries()

    print("What would you like to delete?")
    # Use pickpack module (https://github.com/anafvana/pickpack#map-function-for-nested-lists)
    pass


# Print functions
def print_table(trips):
    trip_console = Console()
    trip_table = Table(title="Itineraries", show_lines=True)

    trip_table.add_column("Trip Name", justify="center", no_wrap=True)
    trip_table.add_column("Location", justify="center")
    trip_table.add_column("Summary", justify="center")
    trip_table.add_column("Start Date", justify="center", no_wrap=True)
    trip_table.add_column("End Date", justify="center", no_wrap=True)
    trip_table.add_column("Flights", justify="left", no_wrap=True)
    trip_table.add_column("Attractions", justify="left", style="bold")

    for trip in trips:
        for key in trip["flights"]:
            if len(key) == 1:
                departure_flight_name = key
                flight_departure = trip["flights"][f"{departure_flight_name}"]["departure date"]
                flight_list = f'[bold red]{departure_flight_name}[/bold red]: {flight_departure}\n'
            elif len(key) >= 2:
                flight_list = ''
                departure_flight_name = key
                flight_departure = trip["flights"][f"{departure_flight_name}"]["departure date"]
                flight_item = f'[bold red]{departure_flight_name}[/bold red]: {flight_departure}\n'
                flight_list = flight_list + f'{flight_item}'
        for key in trip["attractions"]:
            if len(key) == 1:
                attraction = key
                attraction_list = f'[bold red]{attraction}[/bold red] \nAddress: {trip["attractions"][f"{attraction}"]["address"]} \nSummary: {trip["attractions"][f"{attraction}"]["summary"]} \nTag(s): {trip["attractions"][f"{attraction}"]["tag(s)"]}\n'
            elif len(key) >= 2:
                attraction_list = ''
                attraction = key
                # Printing python text with colour using ANSI codes: https://vascosim.medium.com/how-to-print-colored-text-in-python-52f6244e2e30
                attraction_item = f'[bold red]{attraction}[/bold red] \nAddress: {trip["attractions"][f"{attraction}"]["address"]} \nSummary: {trip["attractions"][f"{attraction}"]["summary"]} \nTag(s): {trip["attractions"][f"{attraction}"]["tag(s)"]}\n'
                attraction_list = attraction_list + f'{attraction_item}'
        trip_table.add_row(trip["name"], trip["location"], trip["summary"], trip["start_date"], trip["end_date"], flight_list, attraction_list)
    trip_console.print(trip_table)
    return


# Validation functions

def validate_dates(start_date, end_date, flights):
    '''
    Validate dates given for start date, end date and flight datetimes

    Raises:
        ValueError: If the start or end date is not in the correct format.

    :param start_date (DD-MM-YYYY): Itinerary start date.
    :param end_date (DD-MM-YYYY): Itinerary start date.
    :param flights (nested dict): Nested dictionary containing flight information. This function will be testing the departure_date and arrival_date items.
    '''

    try:
        datetime.strptime(start_date, "%d-%m-%Y")
    except ValueError:
        print("Error: Invalid start date. Use 'DD-MM-YYYY' format.")
        return False

    try:
        datetime.strptime(end_date, "%d-%m-%Y")
    except ValueError:
        print("Error: Invalid end date. Use 'DD-MM-YYYY' format.")
        return False

    # Resource used for following code: https://stackoverflow.com/questions/17322208/multiple-try-codes-in-one-block
    for flight_name, flight_info in flights.items():
        try:
            datetime.strptime(flight_info["departure date"], "%d-%m-%Y %H:%M")
        except ValueError:
            print("Error: Invalid date/time for flight departure. Use 'DD-MM-YYYY HH:MM' format.")
            return False

        try:
            datetime.strptime(flight_info["arrival date"], "%d-%m-%Y %H:%M")
        except ValueError:
            print("Error: Invalid date/time for flight arrival. Use 'DD-MM-YYYY HH:MM' format.")
            return False

    return True


def find_itinerary(itinerary_list, trip_name):
    '''

    Args:
        itinerary_list: List of all itineraries saved to itinerary.bin file.
        trip_name: Name of the trip user wants to view.

    Returns:
        itinerary: The itinerary the user wants to view.
    '''
    return [itinerary for itinerary in itinerary_list if itinerary["name"] == trip_name]

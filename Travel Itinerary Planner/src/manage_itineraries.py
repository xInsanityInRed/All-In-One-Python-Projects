from src.itinerary import Itinerary
from datetime import datetime

"""
This file contains all of the functions needed for the Travel Itinerary Planner.
It allows the user to add, edit, view, delete, and export an itinerary while checking for errors in input.
"""


def add_itinerary(itinerary_list, name, location, summary, start_date, end_date, flights, attractions):
    '''
    Add a new itinerary to the list of itineraries.

    Args:
        itinerary_list (list): The list of existing Itinerary objects.
        location (str): The main city/country the holiday takes place.
        summary (str, optional): A brief summary of the travel plan.
        start_date (str): The date the holiday begins in 'DD-MM-YYYY' format.
        end_date (str): The date the holiday ends in 'DD-MM-YYYY' format.
        flights (nested dict): A nested dictionary type. Flight name (before-after location format, e.g. Perth-Sydney) is tied to a date in 'DD-MM-YYYY' format.
        attractions (nested dict): Dictionary of attractions. Each dictionary key (name of attraction) contains a short description of the attraction (object).

    Returns:
        bool: True if Itinerary is added without issue, otherwise False.

    Side Effects:
        - Saves the updated itinerary list to a file using `update_itinerary`.
    '''

    # Prevent duplicate itineraries
    if any(trip.name == name for trip in itinerary_list):
        print("Error: A trip with this name already exists!")
        return False

    if not validate_dates(start_date, end_date, flights):
        return False

    # Add the new itinerary after validation checks
    itinerary_list.append(Itinerary(name, location, summary, start_date, end_date, flights, attractions))


def edit_itinerary(itinerary_list, chosen_itinerary):
    # Use pickpack module (https://github.com/anafvana/pickpack#map-function-for-nested-lists)
    pass


def view_itineraries(itinerary_list, chosen_itinerary):
    if not itinerary_list:
        print("No itineraries planned!")
    else:
        # Use pick module: Ask if they would like to view all itineraries, or a specific one
        pass
    return


def delete_itinerary(itinerary_list, chosen_itinerary):
    print("What would you like to delete?")
    # Use pickpack module (https://github.com/anafvana/pickpack#map-function-for-nested-lists)
    pass


def export_itinerary(itinerary, chosen_itinerary):
    # Export to .pdf or .csv file
    # Use pick (not pickpack) library to list itineraries by name and location
    pass


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
            datetime.strptime(flight_info["departure_time"], "%d-%m-%Y %H:%M")
        except ValueError:
            print("Error: Invalid date/time for flight departure. Use 'DD-MM-YYYY HH:MM' format.")
            return False

        try:
            datetime.strptime(flight_info["arrival_time"], "%d-%m-%Y %H:%M")
        except ValueError:
            print("Error: Invalid date/time for flight arrival. Use 'DD-MM-YYYY HH:MM' format.")
            return False

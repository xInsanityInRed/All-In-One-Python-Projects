from src.file_handler import load_itineraries, save_itineraries
from datetime import datetime
from pick import pick
from anytree import Node, RenderTree
from pickpack import pickpack, PickPacker, AnyNode
from rich.console import Console
from rich.table import Table
from rich import print
"""
This file contains all of the functions needed for the Travel Itinerary Planner.
It allows the user to add, edit, view, delete, and export an itinerary while checking for errors in input.
"""


def add_itinerary(itinerary_list, name, location, description, start_date, end_date, flights, attractions):
    """
    Docstring for add_itinerary

    Returns:
        bool: True if Itinerary is added without issue, otherwise False.

    Side Effects:
        - Saves the updated itinerary list to a file using `save_itineraries`.
    """
    # TEST: check that all items have been transferred correctly
    print(name)
    print(location)
    print(description)
    print(start_date)
    print(end_date)
    print(flights)
    print(attractions)

    if validate_dates(start_date, end_date, flights):
        # Add the new itinerary after validation checks
        new_itinerary = {
            "name": name,
            "location": location,
            "description": description,
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


def edit_itinerary(itinerary_list, itinerary_option, edit_option, flight_choice, attraction_choice):
    # Edit the itinerary list
    for itinerary in itinerary_list:
        if itinerary["name"] == itinerary_option:
            # Edit DateTime-adjacent data
            if edit_option == "start_date":
                while True:
                    start_date = input("Start date in DD-MM-YYYY: ")
                    if not validate_dates(start_date, itinerary["end_date"], itinerary["flights"]):
                        print("Invalid date. Please ensure it is in DD-MM-YYYY format (e.g., 12-12-2026)")
                    else:
                        itinerary["start_date"] = start_date
                        break
            elif edit_option == "end_date":
                while True:
                    end_date = input("End date in DD-MM-YYYY: ")
                    if not validate_dates(itinerary["start_date"], end_date, itinerary["flights"]):
                        print("Invalid date. Please ensure it is in DD-MM-YYYY format (e.g., 12-12-2026)")
                    else:
                        itinerary["end_date"] = end_date
                        break
            elif edit_option == "departure date":
                for flight_id in itinerary["flights"]:
                    if flight_id["flight name"] == flight_choice:
                        while True:
                            departure = input("Date & time of flight departure (Format: DD-MM-YYYY HH:MM): ")
                            if not validate_dates(itinerary["start_date"], itinerary["end_date"], itinerary["flights"]):
                                print("Invalid date. Please ensure it is in DD-MM-YYYY HH:MM format (e.g., 12-12-2026 08:00)")
                            else:
                                flight_id["departure date"] = departure
                                flight_id["flight name"] = f"{flight_id["departure airport"]} to {flight_id["arrival airport"]}"
                                break
                        break
            elif edit_option == "arrival date":
                for flight_id in itinerary["flights"]:
                    if flight_id["flight name"] == flight_choice:
                        while True:
                            arrival = input("Date & time of flight arrival (Format: DD-MM-YYYY HH:MM): ")
                            if not validate_dates(itinerary["start_date"], itinerary["end_date"], itinerary["flights"]):
                                print("Invalid date & time. Please ensure it is in DD-MM-YYYY HH:MM format (e.g., 12-12-2026 08:00")
                            else:
                                flight_id["arrival date"] = arrival
                                break
                        break
            else:
                # Edit trip's string data (outside of flights & attractions)
                if edit_option == 'name' or edit_option == 'location' or edit_option == 'description':
                    itinerary[edit_option] = input(f"Enter a new {edit_option} for {itinerary['name']}: ")

                # Flights: string type options
                elif edit_option == 'departure airport':
                    airport_leaving = input("Name of airport you are departing from: ")
                    for flight_id in itinerary["flights"]:
                        if flight_id["flight name"] == flight_choice:
                            flight_id["departure airport"] = airport_leaving
                            flight_id["flight name"] = f"{airport_leaving} to {flight_id["arrival airport"]}"
                            break

                elif edit_option == 'arrival airport':
                    arrival_airport = input("Name of airport you are arriving at: ")
                    for flight_id in itinerary["flights"]:
                        if flight_id["flight name"] == flight_choice:
                            flight_id.update({"arrival airport": arrival_airport})
                            flight_id["flight name"] = f"{flight_id["departure airport"]} to {arrival_airport}"
                            break

                # Attractions: string type options
                elif edit_option == 'attraction_name':
                    attraction_id_name = input("Name of the attraction: ")
                    for attraction in itinerary["attractions"]:
                        if attraction["attraction name"] == attraction_choice:
                            attraction.update({"attraction name": attraction_id_name})
                            break
                elif edit_option == 'address':
                    attraction_address = input("New attraction address: ")
                    for attraction in itinerary["attractions"]:
                        if attraction["attraction name"] == attraction_choice:
                            attraction.update({"address": attraction_address})
                            break
                elif edit_option == 'summary':
                    attraction_summary = input("Short summary of the attraction: ")
                    for attraction in itinerary["attractions"]:
                        if attraction["attraction name"] == attraction_choice:
                            attraction.update({"summary": attraction_summary})
                            break
                elif edit_option == 'tag(s)':
                    attraction_tags = input("Provide some tags that categorise what kind of activity this involves.\nExample of format required: hike, exciting, views: ")
                    for attraction in itinerary["attractions"]:
                        if attraction["attraction name"] == attraction_choice:
                            attraction.update({"tag(s)": attraction_tags})
                            break
    save_itineraries(itinerary_list)
    print(itinerary_list)
    return True


def add_new_flight(itinerary_list, itinerary_name, new_flights):
    for itinerary in itinerary_list:
        if itinerary["name"] == itinerary_name:
            for flight in new_flights:
                if flight not in itinerary["flights"]:
                    itinerary["flights"].append(flight)
                else:
                    print(f"Duplicate flight detected: {flight["flight name"]}!")
                    print("This flight will not be added.")
    save_itineraries(itinerary_list)
    print(itinerary_list)
    return True


def add_new_attraction(itinerary_list, itinerary_name, new_attractions):
    for itinerary in itinerary_list:
        if itinerary["name"] == itinerary_name:
            for attraction in new_attractions:
                if attraction not in itinerary["attractions"]:
                    itinerary["attractions"].append(attraction)
                else:
                    print(f"Duplicate attraction detected: {attraction["attraction name"]}!")
                    print("This attraction will not be added.")
    save_itineraries(itinerary_list)
    print(itinerary_list)
    return True


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
    trip_table.add_column("Description", justify="center")
    trip_table.add_column("Start Date", justify="center", no_wrap=True)
    trip_table.add_column("End Date", justify="center", no_wrap=True)
    trip_table.add_column("Flights", justify="left", no_wrap=True)
    trip_table.add_column("Attractions", justify="left", style="bold")

    for trip in trips:
        flight_list = ''
        attraction_list = ''
        if len(trip["flights"]) == 1:
            flight_list = f'[bold red]{flight["flight name"]}[/bold red] \nDepart: {flight["departure date"]}\nArrive: {flight["arrival date"]} \n'
        else:
            for flight in trip["flights"]:
                flight_item = f'[bold red]{flight["flight name"]}[/bold red] \nDepart: {flight["departure date"]}\nArrive: {flight["arrival date"]} \n'
                flight_list = flight_list + f'{flight_item}'

        if len(trip["attractions"]) == 1:
            attraction_list = f'[bold red]{attraction["attraction name"]}[/bold red] \nAddress: {attraction["address"]} \nSummary: {attraction["summary"]} \nTag(s): {attraction["tag(s)"]}\n'
        else:
            for attraction in trip["attractions"]:
                # Printing python text with colour using ANSI codes: https://vascosim.medium.com/how-to-print-colored-text-in-python-52f6244e2e30
                attraction_string = f'[bold red]{attraction["attraction name"]}[/bold red] \nAddress: {attraction["address"]} \nSummary: {attraction["summary"]} \nTag(s): {attraction["tag(s)"]}\n'
                attraction_list = attraction_list + f'{attraction_string}'

        trip_table.add_row(trip["name"], trip["location"], trip["description"], trip["start_date"], trip["end_date"], flight_list, attraction_list)
    trip_console.print(trip_table)
    return


# Validation functions
def validate_dates(start_date, end_date, flights):
    """
    Validate dates given for start date, end date and flight datetime

    Raises:
        ValueError: If the start or end date is not in the correct format.

    :param start_date: Itinerary start date.
    :param end_date: Itinerary end date.
    :param flights: Nested dictionary containing flight information. This function will be testing the departure_date and arrival_date items.
    """

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
    for flight_info in flights:
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
    """

    Args:
        itinerary_list: List of all itineraries saved to itinerary.bin file.
        trip_name: Name of the trip user wants to view.

    Returns:
        itinerary: The itinerary the user wants to view.
    """
    trip = [itinerary for itinerary in itinerary_list if itinerary["name"] == trip_name]
    return trip

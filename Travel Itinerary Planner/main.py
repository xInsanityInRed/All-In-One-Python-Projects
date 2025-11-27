from src.manage_itineraries import add_itinerary, edit_itinerary, view_itineraries, delete_itinerary, export_itinerary
from pick import pick


def user_task_request(request, itinerary_list):
    '''
    Executes a specific request based on user's choice.
    '''
    # Add a new itinerary
    if request == "1":
        flights_list_done = False
        attractions_list_done = False

        print("How exciting! Please provide us information about the trip: \n")
        name = input("Title of the itinerary: ")
        location = input("Location (NA if not applicable): ")
        summary = input("Brief description of trip: ")
        start_date = input("Start date in DD-MM-YYYY: ")
        end_date = input("End date in DD-MM-YYYY: ")
        flights = {}
        attractions = {}

        print("\nNow it is time to add flights!")
        user_flight_choice = input("If you want to skip this step, type SKIP and press 'Enter'. Otherwise, press 'Enter'. ")
        flights_list_done = False

        if user_flight_choice == "SKIP":
            flights = {}
        else:
            while not flights_list_done:
                flight_details = {}

                departure_airport = input("Name of the airport you will depart from: ")
                departure_date = input("Date & time of flight departure (Format: DD-MM-YYYY HH:MM): ")
                arrival_airport = input("Name of the airport you will arrive at: ")
                arrival_date = input("Date & time of flight arrival (Format: DD-MM-YYYY HH:MM): ")
                flight_name = f"{departure_airport} to {arrival_airport}"

                flight_details.update({
                    "departure airport": departure_airport,
                    "departure date": departure_date,
                    "arrival airport": arrival_airport,
                    "arrival date": arrival_date
                    })
                flights[flight_name] = flight_details

                add_another_flight = input("Would you like to add another flight? Type Y (yes) or N (no): ")
                while True:
                    if add_another_flight == "Y":
                        flights_list_done = True
                        break
                    elif add_another_flight == "N":
                        flights_list_done = False
                        break
                    else:
                        print("Invalid answer: Please type Y or N only.")

        print("\nFinally: ATTRACTIONS!")
        user_attractions_choice = input("If you want to skip this step, type SKIP and press 'Enter'. Otherwise, press 'Enter'. ")
        attractions_list_done = False

        if user_attractions_choice == "SKIP":
            attractions = {}
        else:
            while not attractions_list_done:
                attraction_details = {}

                attraction_name = input("Name of attraction: ")
                attraction_address = input("Address of attraction: ")
                attraction_summary = input("Short description of attraction: ")
                attraction_type = input("(Optional) Provide some tags that categorise what kind of activity this involves.\nExample of format required: hike, exciting, views\n")
                attraction_tags = attraction_type.split(", ")

                attraction_details.update({
                    "address": attraction_address,
                    "summary": attraction_summary,
                    "tag(s)": attraction_tags
                    })
                attractions[attraction_name] = attraction_details

                add_another_attraction = input("Would you like to add another attraction? Type Y or N:")
                while True:
                    if add_another_attraction == "Y":
                        attractions_list_done = True
                        break
                    elif add_another_attraction == "N":
                        attractions_list_done = False
                        break
                    else:
                        print("Invalid answer: Please type Y or N only.")

        add_itinerary(itinerary_list, name, location, summary, start_date, end_date, flights, attractions)

    # Edit existing itinerary
    elif request == "2":
        # Use pickpack module (https://github.com/anafvana/pickpack#map-function-for-nested-lists)
        chosen_itinerary = input("")
        edit_itinerary(itinerary_list, chosen_itinerary)
        pass

    # View itinerary
    elif request == "3":
        chosen_itinerary = input("")
        view_itineraries(itinerary_list, chosen_itinerary)
        pass

    # Delete itinerary
    elif request == "4":
        chosen_itinerary = input("")
        delete_itinerary(itinerary_list, chosen_itinerary)
        pass

    # Export itinerary
    elif request == "5":
        chosen_itinerary = input("")
        export_itinerary(itinerary_list, chosen_itinerary)
        pass

    else:
        print("Invalid answer, please type a number between 1-5.")
        return


def run_app():
    """
    Main loop to run the travel planner.
    """
    itineraries = []
    app_running = True

    while app_running:
        print("Welcome to the Travel Itinerary Planner app!\n")
        print("1. Add a new Itinerary")
        print("2. Edit an existing Itinerary")
        print("3. View existing Itineraries")
        print("4. Delete an Itinerary")
        print("5. Export an Itinerary")
        print("6. Log out\n")

        user_choice = input("Please select one of the above options (1-5): ")

        # Check user_choice was a number
        if user_choice.isdigit():
            choice = int(user_choice)
            if 1 <= choice <= 6:
                if user_choice == "6":
                    app_running = False
                else:
                    user_task_request(user_choice, itineraries)
            else:
                print("Enter a number between 1-6.")
        else:
            ("Invalid input: Please enter a number between 1-6.")

    print("See you next time! 👋")
    pass


if __name__ == "__main__":
    run_app()

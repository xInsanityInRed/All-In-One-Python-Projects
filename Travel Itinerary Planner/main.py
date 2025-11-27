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
        while not flights_list_done:
            # Answer format: Perth-Sydney 12-12-2012, Sydney-Perth 21-12-2012
            flights = input("")  # dictionary - add loop here
            if flights == "DONE":
                flights_list_done = True
        while not attractions_list_done:
            attractions = input("")  # dictionary - add loop here
            if attractions == "DONE":
                attractions_list_done = True
        add_itinerary(itinerary_list, name, location, summary, start_date, end_date, flights, attractions)
        pass

    # Edit existing itinerary
    elif request == "2":
        # Use pickpack module (https://github.com/anafvana/pickpack#map-function-for-nested-lists)
        pass
    
    # View itinerary
    elif request == "3":
        view_itineraries(itinerary_list)
        pass

    # Delete itinerary
    elif request == "4":
        delete_itinerary(itinerary_list)
        pass

    elif request == "5":
        # Export to .csv file?
        # Use pick (not pickpack) library to list itineraries by name and location
        export_itinerary(itinerary_list)
        pass

    else:
        print("Invalid answer, please type a number between 1-5.")
        pass


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

class Itinerary:
    """
    This class represents a single itinerary object that users can create.

    Args:
        name (str): The name assigned to the itinerary.
        location (str): The main city/country the holiday takes place.
        summary (str, optional): A brief summary of the travel plan.
        start_date (str): The date the holiday begins in 'DD-MM-YYYY' format.
        end_date (str): The date the holiday ends in 'DD-MM-YYYY' format.
        flights (dict): A nested dictionary type containing flights and flight details:
            flight_name (key, dict type): Contains the flight name (departure-arrival location format, e.g. 'Perth to Sydney')
                departure_airport (str): Departure airport name.
                departure_date (datetime): Date & time of flight departure in 'DD-MM-YYYY HH:MM' format.
                arrival_airport (str): Arrival airport name.
                arrival_date (datetime): Date & time of flight arrival in 'DD-MM-YYYY HH:MM' format.
        attractions (dict): Nested dictionary of attractions. Each dictionary key (name of attraction) contains:
            attraction_name (str, dict): Name of attraction (key) and a dictionary containing attraction details:
                address (str): Address of attraction.
                attraction_summary(str): Short description of attraction.
                attraction_tags (list): List of tags (str type) that catergorise the attraction.
        """

    def __init__(self, name, location, summary, start_date, end_date, flights, attractions):
        self.name = name
        self.location = location
        self.summary = summary
        self.start_date = start_date
        self.end_date = end_date
        self.flights = flights
        self.attractions = attractions
        pass

    def to_dict(self):
        """
        Converts the Itinerary object into a dictionary.

        Returns:
            dict: A dictionary containing itinerary details with these keys:
                'name', 'location', 'summary', 'start-date', 'end-date', 'flights', and 'attractions'.
        """
        return {
            "name": self.name,
            "location": self.location,
            "summary": self.summary,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "flights": self.flights,
            "attractions": self.attractions
        }
    
    @staticmethod
    def from_dict(itinerary_info):
        """
        Creates an Itinerary object from the dictionary representation.

        Args:
            itinerary_info (dict): A dictionary containing itinerary info with these keys:
                'name', 'location', 'summary', 'start-date', 'end-date', 'flights', and 'attractions'.

        Returns:
            Itinerary: A new Itinerary object created from the dictionary data.
        """
        # TODO: Re-write to accommodate the dictionary type, and load its attributes according to their type.
        # Reference that might help: https://stackoverflow.com/questions/56640436/how-to-generically-serialize-and-de-serialize-objects-from-dictionaries
        
        return Itinerary(
            itinerary_info["name"],
            itinerary_info["location"],
            itinerary_info["summary"],
            itinerary_info["start-date"],
            itinerary_info["end_date"],
            itinerary_info["flights"],
            itinerary_info["attractions"]
        )

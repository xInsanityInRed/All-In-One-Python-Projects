import pickle
import os
from pprint import pprint
from src.itinerary import Itinerary

ITINERARY_FILE = "itineraries.bin"


def load_itineraries():
    """
    Load tasks from a binary file using the pickle module.

    Returns:
        dictionary: A dictionary of Itinerary objects loaded from the binary file.
              If the file does not exist, an empty dictionary is returned.
    """
    if os.path.exists(ITINERARY_FILE):
        with open(ITINERARY_FILE, "rb") as file:
            return pickle.load(file)
    return {}


def save_itineraries(itineraries):
    """
    Save a list of itineraries to a binary file using the pickle module.

    Args:
        itineraries (dict): A dictionary containing Itinerary objects to save.

    Side Effects:
        - Writes the serialized itinerary dictionary to ITINERARY_FILE.
        - Overwrites the file if it already exists.
    """
    with open(ITINERARY_FILE, "wb") as file:
        pickle.dump(itineraries, file)

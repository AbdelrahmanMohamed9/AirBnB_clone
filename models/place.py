#!/usr/bin/python3
""" Place Class Defination. """
from models.base_model import BaseModel


class Place(BaseModel):
    """ Class Represents place.
    Attributes:

        city_id (string): City id.
        user_id (string): User id.
        name (string): Name of the place.
        description (string): Description of the place.
        number_rooms (integer): Number of rooms of the place.
        number_bathrooms (integer): Number of bathrooms of the place.
        max_guest (integer): Maximum number of guests of the place.
        price_by_night (integer): Price by night of the place.
        latitude (float): Latitude of the place.
        longitude (float): Longitude of the place.
        amenity_ids (list): List of Amenity ids.
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = ""
    number_bathrooms = ""
    max_guest = ""
    price_by_night = ""
    latitude = ""
    longitude = ""
    amenity_ids = ""

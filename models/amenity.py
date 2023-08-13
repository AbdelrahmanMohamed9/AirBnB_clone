#!/usr/bin/python3
"""defines The amenity Class"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """represent A Amenity

    attributes:
        Name (str): the Name Of The Amenity
    """

    name = ""

#!/usr/bin/python3
"""defines The city Class"""
from models.base_model import BaseModel


class City(BaseModel):
    """represent An city

    Attributes:
        state_id (str): the State Id
        name (str): the Name Of The City
    """

    state_id = ""
    name = ""

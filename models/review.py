#!/usr/bin/python3
""" Rview Class Defination. """
from models.base_model import BaseModel


class Review(BaseModel):
    """ Review Class Represnation.
    Attriputes:

        place_id (string): Place id.
        user_id (string): User id.
        text (string): Text of the review.
    """

    place_id = ""
    user_id = ""
    text = ""

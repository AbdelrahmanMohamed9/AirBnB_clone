#!/usr/bin/python3
"""defines The baseModel Class"""
import models
from datetime import datetime
from uuid import uuid4


class BaseModel:
    """represents The baseModel Of The HBnB Project"""

    def __init__(self, *args, **kwargs):
        """initialize A New baseModel

        Args:
            *args (any): unused
            **kwargs (dict): Key/Value Pairs Of Attributes
        """
        tfrm = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, tfrm)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def save(self):
        """Update Updated_at With The Current Datetime"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """return The Dictionary Of The daseModel Instance

        includes The key/Value Pair __class__ Representing
        A Class Name Of The Object
        """
        rdct = self.__dict__.copy()
        rdct["created_at"] = self.created_at.isoformat()
        rdct["updated_at"] = self.updated_at.isoformat()
        rdct["__class__"] = self.__class__.__name__
        return rdct

    def __str__(self):

        """return The Print/Str Representation Of THE baseModel Instance"""
        clnme = self.__class__.__name__
        return "[{}] ({}) {}".format(clnme, self.id, self.__dict__)

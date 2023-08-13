#!/usr/bin/python3
"""defines A fileStorage Class"""
import json
from models.state import State
from models.city import City
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """represent A Abstracted Storage Engine

    attributes:
        __file_path (str): the Name Of The File To Save Objects To
        __objects (dict): the Dictionary Of THE Instantiated Objects
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """return The Dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """set In __objects Obj With key <obj_class_name>.id ."""
        ocnme = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ocnme, obj.id)] = obj

    def save(self):
        """serialize __objects To The jSON file __file_path"""
        odct = FileStorage.__objects
        objdict = {obj: odct[obj].to_dict() for obj in odct.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """deserialize The JSON File __file_path to __objects, If It Exists"""
        try:
            with open(FileStorage.__file_path) as f:
                objdct = json.load(f)
                for o in objdct.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return

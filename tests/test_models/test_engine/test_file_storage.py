#!/usr/bin/python3
'''defines Unittests For Models/Engine/file_storage.py

unittest Classes:
    testFileStorage_instantiation
    testFileStorage_methods
'''
import models
import unittest
import os
import json
from models.user import User
from models.state import State
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.city import City

class TestFileStorage_instantiation(unittest.TestCase):
    '''unittests For Testing Instantiation Of The fileStorage Class'''

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    '''unittests For Testing Methods Of The fileStorage Class'''

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        bm = BaseModel()
        usr = User()
        sst = State()
        ppl = Place()
        cy = City()
        am = Amenity()
        rev = Review()
        models.storage.new(bm)
        models.storage.new(usr)
        models.storage.new(sst)
        models.storage.new(ppl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rev)
        self.assertIn("BaseModel." + bm.id, models.storage.all().keys())
        self.assertIn(bm, models.storage.all().values())
        self.assertIn("User." + usr.id, models.storage.all().keys())
        self.assertIn(usr, models.storage.all().values())
        self.assertIn("State." + sst.id, models.storage.all().keys())
        self.assertIn(sst, models.storage.all().values())
        self.assertIn("Place." + ppl.id, models.storage.all().keys())
        self.assertIn(ppl, models.storage.all().values())
        self.assertIn("City." + cy.id, models.storage.all().keys())
        self.assertIn(cy, models.storage.all().values())
        self.assertIn("Amenity." + am.id, models.storage.all().keys())
        self.assertIn(am, models.storage.all().values())
        self.assertIn("Review." + rv.id, models.storage.all().keys())
        self.assertIn(rev, models.storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        bm = BaseModel()
        usr = User()
        sst = State()
        ppl = Place()
        cy = City()
        am = Amenity()
        rev = Review()
        models.storage.new(bm)
        models.storage.new(usr)
        models.storage.new(sst)
        models.storage.new(ppl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rev)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + bm.id, save_text)
            self.assertIn("User." + usr.id, save_text)
            self.assertIn("State." + sst.id, save_text)
            self.assertIn("Place." + ppl.id, save_text)
            self.assertIn("City." + cy.id, save_text)
            self.assertIn("Amenity." + am.id, save_text)
            self.assertIn("Review." + rev.id, save_text)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        bm = BaseModel()
        usr = User()
        sst = State()
        ppl = Place()
        cy = City()
        am = Amenity()
        rev = Review()
        models.storage.new(bm)
        models.storage.new(usr)
        models.storage.new(sst)
        models.storage.new(ppl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rev)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bm.id, objs)
        self.assertIn("User." + usr.id, objs)
        self.assertIn("State." + sst.id, objs)
        self.assertIn("Place." + ppl.id, objs)
        self.assertIn("City." + cy.id, objs)
        self.assertIn("Amenity." + am.id, objs)
        self.assertIn("Review." + rev.id, objs)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/python3
""" Unitests for amenity.py.

Unittest classes:
    TestAmenity_instantiate
    TestAmenity_save
    TestAmenity_to_dict
"""

import os
import unittest
import models
from time import sleep
from datetime import datetime
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """ Unitest for testing the instantiation of the 
    Amenity calss.
    """

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_two_amenities_unique_ids(self):
        amn1 = Amenity()
        amn2 = Amenity()
        self.assertNotEqual(amn1.id, amn2.id)

    def test_name_is_public_class_attribute(self):
        amn = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amn.__dict__)

    def test_two_amenities_different_updated_at(self):
        amn1 = Amenity()
        sleep(0.05)
        amn2 = Amenity()
        self.assertLess(amn1.updated_at, amn2.updated_at)

    def test_two_amenities_different_created_at(self):
        amn1 = Amenity()
        sleep(0.05)
        amn2 = Amenity()
        self.assertLess(amn1.created_at, amn2.created_at)

    def test_str_representation(self):
        dat = datetime.today()
        dat_repr = repr(dat)
        amn = Amenity()
        amn.id = "123456"
        amn.created_at = amn.updated_at = dat
        amnstr = amn.__str__()
        self.assertIn("[Amenity] (123456)", amnstr)
        self.assertIn("'id': '123456'", amnstr)
        self.assertIn("'created_at': " + dat_repr, amnstr)
        self.assertIn("'updated_at': " + dat_repr, amnstr)

    def test_args_unused(self):
        amn = Amenity(None)
        self.assertNotIn(None, amn.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """instantiation with kwargs test method"""
        dat = datetime.today()
        dat_iso = dat.isoformat()
        amn = Amenity(id="345", created_at=dat_iso, updated_at=dat_iso)
        self.assertEqual(amn.id, "345")
        self.assertEqual(amn.created_at, dat)
        self.assertEqual(amn.updated_at, dat)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """ Unittests for testing the  save method 
    of the Amenity class.
    """

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        amn = Amenity()
        sleep(0.05)
        first_updated_at = amn.updated_at
        amn.save()
        self.assertLess(first_updated_at, amn.updated_at)

    def test_two_saves(self):
        amn = Amenity()
        sleep(0.05)
        first_updated_at = amn.updated_at
        amn.save()
        second_updated_at = amn.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amn.save()
        self.assertLess(second_updated_at, am.updated_at)

    def test_save_with_arg(self):
        amn = Amenity()
        with self.assertRaises(TypeError):
            amn.save(None)

    def test_save_updates_file(self):
        amn = Amenity()
        amn.save()
        amnid = "Amenity." + amn.id
        with open("file.json", "r") as f:
            self.assertIn(amnid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """ Unittests for testing the to_dict method 
    of the Amenity class.
    """

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_added_attributes(self):
        amn = Amenity()
        amn.middle_name = "Holberton"
        amn.my_number = 98
        self.assertEqual("Holberton", amn.middle_name)
        self.assertIn("my_number", amn.to_dict())

    def test_to_dict_contains_correct_keys(self):
        amn = Amenity()
        self.assertIn("id", amn.to_dict())
        self.assertIn("created_at", amn.to_dict())
        self.assertIn("updated_at", amn.to_dict())
        self.assertIn("__class__", amn.to_dict())

    def test_to_dict_output(self):
        dat = datetime.today()
        amn = Amenity()
        amn.id = "123456"
        amn.created_at = amn.updated_at = dat
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dat.isoformat(),
            'updated_at': dat.isoformat(),
        }
        self.assertDictEqual(amn.to_dict(), tdict)

    def test_to_dict_datetime_attributes_are_strs(self):
        amn = Amenity()
        amn_dict = amn.to_dict()
        self.assertEqual(str, type(amn_dict["id"]))
        self.assertEqual(str, type(amn_dict["created_at"]))
        self.assertEqual(str, type(amn_dict["updated_at"]))

    def test_contrast_to_dict_dunder_dict(self):
        amn = Amenity()
        self.assertNotEqual(amn.to_dict(), amn.__dict__)

    def test_to_dict_with_arg(self):
        amn = Amenity()
        with self.assertRaises(TypeError):
            amn.to_dict(None)


if __name__ == "__main__":
    unittest.main()

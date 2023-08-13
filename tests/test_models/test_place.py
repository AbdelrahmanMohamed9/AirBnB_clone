#!/usr/bin/python3
'''defines Unittests For Models/Place.py

unittest Classes:
    testPlace_instantiation
    testPlace_save
    testPlace_to_dict
'''
import models
import unittest
import os
from time import sleep
from models.place import Place
from datetime import datetime

class TestPlace_instantiation(unittest.TestCase):
    '''unittests For Testing Instantiation Of The Place Class'''

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_attribute(self):
        ppl = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(ppl))
        self.assertNotIn("city_id", ppl.__dict__)

    def test_user_id_is_public_class_attribute(self):
        ppl = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(ppl))
        self.assertNotIn("user_id", ppl.__dict__)

    def test_name_is_public_class_attribute(self):
        ppl = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(ppl))
        self.assertNotIn("name", ppl.__dict__)

    def test_description_is_public_class_attribute(self):
        ppl = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(ppl))
        self.assertNotIn("desctiption", ppl.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        ppl = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(ppl))
        self.assertNotIn("number_rooms", ppl.__dict__)

    def test_number_bathrooms_is_public_class_attribute(self):
        ppl = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(ppl))
        self.assertNotIn("number_bathrooms", ppl.__dict__)

    def test_max_guest_is_public_class_attribute(self):
        ppl = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(ppl))
        self.assertNotIn("max_guest", ppl.__dict__)

    def test_price_by_night_is_public_class_attribute(self):
        ppl = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(ppl))
        self.assertNotIn("price_by_night", ppl.__dict__)

    def test_latitude_is_public_class_attribute(self):
        ppl = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(ppl))
        self.assertNotIn("latitude", ppl.__dict__)

    def test_longitude_is_public_class_attribute(self):
        ppl = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(ppl))
        self.assertNotIn("longitude", ppl.__dict__)

    def test_amenity_ids_is_public_class_attribute(self):
        ppl = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(ppl))
        self.assertNotIn("amenity_ids", ppl.__dict__)

    def test_two_places_unique_ids(self):
        ppl1 = Place()
        ppl2 = Place()
        self.assertNotEqual(ppl1.id, ppl2.id)

    def test_two_places_different_created_at(self):
        ppl1 = Place()
        sleep(0.05)
        ppl2 = Place()
        self.assertLess(ppl1.created_at, ppl2.created_at)

    def test_two_places_different_updated_at(self):
        ppl1 = Place()
        sleep(0.05)
        ppl2 = Place()
        self.assertLess(ppl1.updated_at, ppl2.updated_at)

    def test_str_representation(self):
        ddt = datetime.today()
        ddt_rp = repr(dt)
        ppl = Place()
        ppl.id = "123456"
        ppl.created_at = pl.updated_at = dt
        pplstr = pl.__str__()
        self.assertIn("[Place] (123456)", pplstr)
        self.assertIn("'id': '123456'", pplstr)
        self.assertIn("'created_at': " + ddt_rp, pplstr)
        self.assertIn("'updated_at': " + ddt_rp, pplstr)

    def test_args_unused(self):
        ppl = Place(None)
        self.assertNotIn(None, ppl.__dict__.values())

    def test_instantiation_with_kwargs(self):
        ddt = datetime.today()
        ddt_is = dt.isoformat()
        ppl = Place(id="345", created_at=ddt_is, updated_at=ddt_is)
        self.assertEqual(ppl.id, "345")
        self.assertEqual(ppl.created_at, ddt)
        self.assertEqual(ppl.updated_at, ddt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    '''unittests For Testing Save Method Of The Place Class'''

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
        ppl = Place()
        sleep(0.05)
        first_updated_at = ppl.updated_at
        ppl.save()
        self.assertLess(first_updated_at, ppl.updated_at)

    def test_two_saves(self):
        ppl = Place()
        sleep(0.05)
        frst_updted_at = ppl.updated_at
        ppl.save()
        sec_updted_at = ppl.updated_at
        self.assertLess(frst_updted_at, sec_updted_at)
        sleep(0.05)
        ppl.save()
        self.assertLess(sec_updted_at, ppl.updated_at)

    def test_save_with_arg(self):
        ppl = Place()
        with self.assertRaises(TypeError):
            ppl.save(None)

    def test_save_updates_file(self):
        ppl = Place()
        ppl.save()
        pplid = "Place." + ppl.id
        with open("file.json", "r") as f:
            self.assertIn(pplid, f.read())


class TestPlace_to_dict(unittest.TestCase):
    '''unittests For Testing to_dict Method Of The Place Class'''

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        ppl = Place()
        self.assertIn("id", ppl.to_dict())
        self.assertIn("created_at", ppl.to_dict())
        self.assertIn("updated_at", ppl.to_dict())
        self.assertIn("__class__", ppl.to_dict())

    def test_to_dict_contains_added_attributes(self):
        ppl = Place()
        ppl.mid_name = "Holberton"
        ppl.my_num = 98
        self.assertEqual("Holberton", ppl.mid_name)
        self.assertIn("my_number", ppl.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        ppl = Place()
        ppl_dict = ppl.to_dict()
        self.assertEqual(str, type(ppl_dict["id"]))
        self.assertEqual(str, type(ppl_dict["created_at"]))
        self.assertEqual(str, type(ppl_dict["updated_at"]))

    def test_to_dict_output(self):
        ddt = datetime.today()
        ppl = Place()
        ppl.id = "123456"
        ppl.creted_at = pl.updated_at = ddt
        xdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': ddt.isoformat(),
            'updated_at': ddt.isoformat(),
        }
        self.assertDictEqual(ppl.to_dict(), xdict)

    def test_contrast_to_dict_dunder_dict(self):
        ppl = Place()
        self.assertNotEqual(ppl.to_dict(), ppl.__dict__)

    def test_to_dict_with_arg(self):
        ppl = Place()
        with self.assertRaises(TypeError):
            ppl.to_dict(None)


if __name__ == "__main__":
    unittest.main()

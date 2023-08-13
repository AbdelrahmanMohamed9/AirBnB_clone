#!/usr/bin/python3
'''defines Unittests For Models/State.py

unittest classes:
    testState_instantiation
    testState_save
    testState_to_dict
'''
import models
import unittest
import os
from time import sleep
from models.state import State
from datetime import datetime

class TestState_instantiation(unittest.TestCase):
    '''unittests For Testing Instantiation Of The state Class'''

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        s = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(sst))
        self.assertNotIn("name", sst.__dict__)

    def test_two_states_unique_ids(self):
        sst1 = State()
        sst2 = State()
        self.assertNotEqual(sst1.id, sst2.id)

    def test_two_states_different_created_at(self):
        sst1 = State()
        sleep(0.05)
        sst2 = State()
        self.assertLess(sst1.created_at, sst2.created_at)

    def test_two_states_different_updated_at(self):
        sst1 = State()
        sleep(0.05)
        sst2 = State()
        self.assertLess(sst1.updated_at, sst2.updated_at)

    def test_str_representation(self):
        ddt = datetime.today()
        ddt_rep = repr(ddt)
        sst = State()
        sst.id = "123456"
        sst.creted_at = sst.updated_at = ddt
        sststr = st.__str__()
        self.assertIn("[State] (123456)", sststr)
        self.assertIn("'id': '123456'", sststr)
        self.assertIn("'created_at': " + ddt_rep, sststr)
        self.assertIn("'updated_at': " + ddt_rep, sststr)

    def test_args_unused(self):
        sst = State(None)
        self.assertNotIn(None, sst.__dict__.values())

    def test_instantiation_with_kwargs(self):
        ddt = datetime.today()
        ddt_iso = ddt.isoformat()
        sst = State(id="345", created_at=ddt_iso, updated_at=ddt_iso)
        self.assertEqual(sst.id, "345")
        self.assertEqual(sst.created_at, ddt)
        self.assertEqual(sst.updated_at, ddt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    '''unittests For Testing Save Method Of The state Class'''

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
        sst = State()
        sleep(0.05)
        frst_updted_at = sst.updated_at
        sst.save()
        self.assertLess(frst_updted_at, sst.updated_at)

    def test_two_saves(self):
        sst = State()
        sleep(0.05)
        frst_updted_at = sst.updated_at
        sst.save()
        sec_updted_at = sst.updated_at
        self.assertLess(frst_updted_at, sec_updted_at)
        sleep(0.05)
        sst.save()
        self.assertLess(sec_updted_at, sst.updated_at)

    def test_save_with_arg(self):
        sst = State()
        with self.assertRaises(TypeError):
            sst.save(None)

    def test_save_updates_file(self):
        sst = State()
        sst.save()
        sstid = "State." + sst.id
        with open("file.json", "r") as f:
            self.assertIn(sstid, f.read())


class TestState_to_dict(unittest.TestCase):
    '''unittests For Testing to_dict Method Of The state Class'''

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        sst = State()
        self.assertIn("id", sst.to_dict())
        self.assertIn("created_at", sst.to_dict())
        self.assertIn("updated_at", sst.to_dict())
        self.assertIn("__class__", sst.to_dict())

    def test_to_dict_contains_added_attributes(self):
        sst = State()
        sst.mid_name = "Holberton"
        sst.my_num = 98
        self.assertEqual("Holberton", sst.mid_name)
        self.assertIn("my_number", sst.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        sst = State()
        sst_dict = sst.to_dict()
        self.assertEqual(str, type(sst_dict["id"]))
        self.assertEqual(str, type(sst_dict["created_at"]))
        self.assertEqual(str, type(sst_dict["updated_at"]))

    def test_to_dict_output(self):
        ddt = datetime.today()
        sst = State()
        sst.id = "123456"
        sst.created_at = sst.updated_at = ddt
        xdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': ddt.isoformat(),
            'updated_at': ddt.isoformat(),
        }
        self.assertDictEqual(sst.to_dict(), xdict)

    def test_contrast_to_dict_dunder_dict(self):
        sst = State()
        self.assertNotEqual(sst.to_dict(), sst.__dict__)

    def test_to_dict_with_arg(self):
        sst = State()
        with self.assertRaises(TypeError):
            sst.to_dict(None)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/python3
""" Unittests for base_model.py.
Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""

import os
import unittest
import models
from time import sleep
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """ Unittests for the testing instantiation
    of the BaseModel class.
    """

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_two_models_unique_ids(self):
        bsm1 = BaseModel()
        bsm2 = BaseModel()
        self.assertNotEqual(bsm1.id, bsm2.id)

    def test_two_models_different_updated_at(self):
        bsm1 = BaseModel()
        sleep(0.05)
        bsm2 = BaseModel()
        self.assertLess(bsm1.updated_at, bsm2.updated_at)

    def test_two_models_different_created_at(self):
        bsm1 = BaseModel()
        sleep(0.05)
        bsm2 = BaseModel()
        self.assertLess(bsm1.created_at, bsm2.created_at)

    def test_args_unused(self):
        bsm = BaseModel(None)
        self.assertNotIn(None, bsm.__dict__.values())

    def test_str_representation(self):
        dat = datetime.today()
        dat_repr = repr(dat)
        bsm = BaseModel()
        bsm.id = "123456"
        bsm.created_at = bsm.updated_at = dat
        bsmstr = bsm.__str__()
        self.assertIn("[BaseModel] (123456)", bsmstr)
        self.assertIn("'id': '123456'", bsmstr)
        self.assertIn("'created_at': " + dat_repr, bsmstr)
        self.assertIn("'updated_at': " + dat_repr, bsmstr)

    def test_instantiation_with_kwargs(self):
        dat = datetime.today()
        dat_iso = dat.isoformat()
        bsm = BaseModel(id="345", created_at=dat_iso, updated_at=dat_iso)
        self.assertEqual(bsm.id, "345")
        self.assertEqual(bsm.created_at, dat)
        self.assertEqual(bsm.updated_at, dat)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dat = datetime.today()
        dat_iso = dat.isoformat()
        bsm = BaseModel("12", id="345", created_at=dat_iso, updated_at=dat_iso)
        self.assertEqual(bsm.id, "345")
        self.assertEqual(bsm.created_at, dat)
        self.assertEqual(bsm.updated_at, dat)


class TestBaseModel_save(unittest.TestCase):
    """ Unittests for testing save method of
    BaseModel class.
    """

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

    def test_one_save(self):
        bsm = BaseModel()
        sleep(0.05)
        first_updated_at = bsm.updated_at
        bsm.save()
        self.assertLess(first_updated_at, bsm.updated_at)

    def test_two_saves(self):
        bsm = BaseModel()
        sleep(0.05)
        first_updated_at = bsm.updated_at
        bsm.save()
        second_updated_at = bsm.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        bsm.save()
        self.assertLess(second_updated_at, bsm.updated_at)

    def test_save_updates_file(self):
        bsm = BaseModel()
        bsm.save()
        bsmid = "BaseModel." + bsm.id
        with open("file.json", "r") as f:
            self.assertIn(bsmid, f.read())

    def test_save_with_arg(self):
        bsm = BaseModel()
        with self.assertRaises(TypeError):
            bsm.save(None)


class TestBaseModel_to_dict(unittest.TestCase):
    """ Unittests for testing to_dict method of
    the BaseModel class.
    """

    def test_to_dict_type(self):
        bsm = BaseModel()
        self.assertTrue(dict, type(bsm.to_dict()))

    def test_to_dict_contains_added_attributes(self):
        bsm = BaseModel()
        bsm.name = "Holberton"
        bsm.my_number = 98
        self.assertIn("name", bsm.to_dict())
        self.assertIn("my_number", bsm.to_dict())

    def test_to_dict_contains_correct_keys(self):
        bsm = BaseModel()
        self.assertIn("id", bsm.to_dict())
        self.assertIn("created_at", bsm.to_dict())
        self.assertIn("updated_at", bsm.to_dict())
        self.assertIn("__class__", bsm.to_dict())

    def test_to_dict_output(self):
        dat = datetime.today()
        bsm = BaseModel()
        bsm.id = "123456"
        bsm.created_at = bsm.updated_at = dat
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dat.isoformat(),
            'updated_at': dat.isoformat()
        }
        self.assertDictEqual(bsm.to_dict(), tdict)

    def test_to_dict_datetime_attributes_are_strs(self):
        bsm = BaseModel()
        bsm_dict = bsm.to_dict()
        self.assertEqual(str, type(bsm_dict["created_at"]))
        self.assertEqual(str, type(bsm_dict["updated_at"]))

    def test_contrast_to_dict_dunder_dict(self):
        bsm = BaseModel()
        self.assertNotEqual(bsm.to_dict(), bsm.__dict__)

    def test_to_dict_with_arg(self):
        bsm = BaseModel()
        with self.assertRaises(TypeError):
            bsm.to_dict(None)


if __name__ == "__main__":
    unittest.main()

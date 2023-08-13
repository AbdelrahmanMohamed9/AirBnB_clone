#!/usr/bin/python3
'''defines Unittests For Models/Review.py

unittest Classes:
    testReview_instantiation
    testReview_save
    testReview_to_dict
'''
import models
import unittest
import os
from time import sleep
from models.review import Review
from datetime import datetime

class TestReview_instantiation(unittest.TestCase):
    '''unittests For Testing Instantiation Of The review Class'''

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        rev = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(rev))
        self.assertNotIn("place_id", rev.__dict__)

    def test_user_id_is_public_class_attribute(self):
        rev = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(rev))
        self.assertNotIn("user_id", rev.__dict__)

    def test_text_is_public_class_attribute(self):
        rev = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(rev))
        self.assertNotIn("text", rev.__dict__)

    def test_two_reviews_unique_ids(self):
        rev1 = Review()
        rev2 = Review()
        self.assertNotEqual(rev1.id, rev2.id)

    def test_two_reviews_different_created_at(self):
        rev1 = Review()
        sleep(0.05)
        rev2 = Review()
        self.assertLess(rev1.created_at, rev2.created_at)

    def test_two_reviews_different_updated_at(self):
        rev1 = Review()
        sleep(0.05)
        rev2 = Review()
        self.assertLess(rev1.updated_at, rev2.updated_at)

    def test_str_representation(self):
        ddt = datetime.today()
        ddt_rep = repr(dt)
        rev = Review()
        rev.id = "123456"
        rev.creted_at = rev.updated_at = dt
        revstr = rv.__str__()
        self.assertIn("[Review] (123456)", revstr)
        self.assertIn("'id': '123456'", revstr)
        self.assertIn("'created_at': " + ddt_rep, revstr)
        self.assertIn("'updated_at': " + ddt_rep, revstr)

    def test_args_unused(self):
        rev = Review(None)
        self.assertNotIn(None, rev.__dict__.values())

    def test_instantiation_with_kwargs(self):
        ddt = datetime.today()
        ddt_is = dt.isoformat()
        rev = Review(id="345", created_at=ddt_is, updated_at=ddt_is)
        self.assertEqual(rev.id, "345")
        self.assertEqual(rev.creted_at, ddt)
        self.assertEqual(rev.updated_at, ddt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    '''unittests For Testing Save Method Of The review Class'''

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
        rev = Review()
        sleep(0.05)
        frst_updted_at = rev.updated_at
        rev.save()
        self.assertLess(first_updted_at, rev.updated_at)

    def test_two_saves(self):
        rev = Review()
        sleep(0.05)
        frst_updted_at = rev.updated_at
        rev.save()
        sec_updted_at = rev.updated_at
        self.assertLess(frst_updted_at, sec_updted_at)
        sleep(0.05)
        rev.save()
        self.assertLess(sec_updted_at, rev.updated_at)

    def test_save_with_arg(self):
        rev = Review()
        with self.assertRaises(TypeError):
            rev.save(None)

    def test_save_updates_file(self):
        rev = Review()
        rev.save()
        revid = "Review." + rev.id
        with open("file.json", "r") as f:
            self.assertIn(revid, f.read())


class TestReview_to_dict(unittest.TestCase):
    '''unittests For Testing to_dict Method Of The review Class'''

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        rev = Review()
        self.assertIn("id", rev.to_dict())
        self.assertIn("created_at", rev.to_dict())
        self.assertIn("updated_at", rev.to_dict())
        self.assertIn("__class__", rev.to_dict())

    def test_to_dict_contains_added_attributes(self):
        rev = Review()
        rev.mid_name = "Holberton"
        rev.my_num = 98
        self.assertEqual("Holberton", rev.mid_name)
        self.assertIn("my_number", rev.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        rev = Review()
        rev_dict = rev.to_dict()
        self.assertEqual(str, type(rev_dict["id"]))
        self.assertEqual(str, type(rev_dict["created_at"]))
        self.assertEqual(str, type(rev_dict["updated_at"]))

    def test_to_dict_output(self):
        ddt = datetime.today()
        rev = Review()
        rev.id = "123456"
        rev.creted_at = rev.updated_at = ddt
        xdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': ddt.isoformat(),
            'updated_at': ddt.isoformat(),
        }
        self.assertDictEqual(rdv.to_dict(), xdict)

    def test_contrast_to_dict_dunder_dict(self):
        rev = Review()
        self.assertNotEqual(rev.to_dict(), rev.__dict__)

    def test_to_dict_with_arg(self):
        rev = Review()
        with self.assertRaises(TypeError):
            rev.to_dict(None)


if __name__ == "__main__":
    unittest.main()

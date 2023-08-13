#!/usr/bin/python3
'''defines Unittests For Console.py

unittest Classes:
    testHBNBCommand_prompting
    testHBNBCommand_help
    testHBNBCommand_exit
    testHBNBCommand_create
    testHBNBCommand_show
    testHBNBCommand_all
    testHBNBCommand_destroy
    testHBNBCommand_update
'''
import sys
import unittest
import os
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch
from models import storage
from models.engine.file_storage import FileStorage

class TestHBNBCommand_prompting(unittest.TestCase):
    '''unittests For Testing Prompting Of The HBNB Command Interpreter'''

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())


class TestHBNBCommand_help(unittest.TestCase):
    '''unittests For Testing Help Messages Of The HBNB Command Interpreter'''

    def test_help_quit(self):
        g = "Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(g, output.getvalue().strip())

    def test_help_create(self):
        g = ("Usage: create <class>\n        "
             "Create a new class instance and print its id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(g, output.getvalue().strip())

    def test_help_EOF(self):
        g = "EOF signal to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(g, output.getvalue().strip())

    def test_help_show(self):
        g = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
             "Display the string representation of a class instance of"
             " a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(g, output.getvalue().strip())

    def test_help_destroy(self):
        g = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n        "
             "Delete a class instance of a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(g, output.getvalue().strip())

    def test_help_all(self):
        g = ("Usage: all or all <class> or <class>.all()\n        "
             "Display string representations of all instances of a given class"
             ".\n        If no class is specified, displays all instantiated "
             "objects.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(g, output.getvalue().strip())

    def test_help_count(self):
        g = ("Usage: count <class> or <class>.count()\n        "
             "Retrieve the number of instances of a given class.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(h, output.getvalue().strip())

    def test_help_update(self):
        g = ("Usage: update <class> <id> <attribute_name> <attribute_value> or"
             "\n       <class>.update(<id>, <attribute_name>, <attribute_value"
             ">) or\n       <class>.update(<id>, <dictionary>)\n        "
             "Update a class instance of a given id by adding or updating\n   "
             "     a given attribute key/value pair or dictionary.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(g, output.getvalue().strip())

    def test_help(self):
        g = ("Documented commands (type help <topic>):\n"
             "-------------------------------------\n"
             "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(g, output.getvalue().strip())


class TestHBNBCommand_exit(unittest.TestCase):
    '''unittests For Testing Exiting From The HBNB Command Interpreter'''

    def test_quit_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommand_create(unittest.TestCase):
    '''unittests For Testing Create From The HBNB Command Interpreter'''

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_create_missing_class(self):
        corect = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_create_invalid_class(self):
        corect = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_create_invalid_syntax(self):
        corect = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(corect, output.getvalue().strip())
        corect = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_create_object(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(output.getvalue().strip()))
            tstKey = "BaseModel.{}".format(output.getvalue().strip())
            self.assertIn(tstKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(output.getvalue().strip()))
            tstKey = "User.{}".format(output.getvalue().strip())
            self.assertIn(tstKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(output.getvalue().strip()))
            tstKey = "State.{}".format(output.getvalue().strip())
            self.assertIn(tstKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(output.getvalue().strip()))
            tstKey = "City.{}".format(output.getvalue().strip())
            self.assertIn(tstKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(output.getvalue().strip()))
            tstKey = "Amenity.{}".format(output.getvalue().strip())
            self.assertIn(tstKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(output.getvalue().strip()))
            tstKey = "Place.{}".format(output.getvalue().strip())
            self.assertIn(tstKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(output.getvalue().strip()))
            tstKey = "Review.{}".format(output.getvalue().strip())
            self.assertIn(tstKey, storage.all().keys())


class TestHBNBCommand_show(unittest.TestCase):
    '''unittests For Testing Show From The HBNB Command Interpreter.'''

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_show_missing_class(self):
        corect = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_show_invalid_class(self):
        corect = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_show_missing_id_space_notation(self):
        corect = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_show_missing_id_dot_notation(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_show_no_instance_found_space_notation(self):
        corect = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review 1"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_show_no_instance_found_dot_notation(self):
        corect = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
            self.assertEqual(corect, output.getvalue().strip())


    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(tstID)]
            comand = "show BaseModel {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(tstID)]
            comand = "show User {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(tstID)]
            comand = "show State {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(tstID)]
            comand = "show Place {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(tstID)]
            comand = "show City {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(tstID)]
            comand = "show Amenity {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(tstID)]
            comand = "show Review {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertEqual(obj.__str__(), output.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(tstID)]
            comand = "BaseModel.show({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(tstID)]
            comand = "User.show({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(tstID)]
            command = "State.show({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(tstID)]
            command = "Place.show({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(tstID)]
            comand = "City.show({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(tstID)]
            command = "Amenity.show({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertEqual(obj.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(tstID)]
            comand = "Review.show({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertEqual(obj.__str__(), output.getvalue().strip())


class TestHBNBCommand_destroy(unittest.TestCase):
    '''unittests For Testing Destroy From The HBNB Command Interpreter'''

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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
        storage.reload()

    def test_destroy_missing_class(self):
        corect = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_destroy_invalid_class(self):
        corect = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_destroy_id_missing_space_notation(self):
        corect = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_destroy_id_missing_dot_notation(self):
        corect = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_destroy_invalid_id_space_notation(self):
        corect = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy User 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy State 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy City 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_destroy_invalid_id_dot_notation(self):
        corect = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_destroy_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(tstID)]
            comand = "destroy BaseModel {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(tstID)]
            command = "show User {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(tstID)]
            command = "show State {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(testID)]
            comand = "show Place {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(tstID)]
            comand = "show City {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(tstID)]
            comand = "show Amenity {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(tstID)]
            comand = "show Review {}".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertNotIn(obj, storage.all())

    def test_destroy_objects_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["BaseModel.{}".format(tstID)]
            comand = "BaseModel.destroy({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["User.{}".format(tstID)]
            comand = "User.destroy({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["State.{}".format(tstID)]
            comand = "State.destroy({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Place.{}".format(tstID)]
            comand = "Place.destroy({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["City.{}".format(tstID)]
            comand = "City.destroy({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Amenity.{}".format(tstID)]
            comand = "Amenity.destroy({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            tstID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            obj = storage.all()["Review.{}".format(tstID)]
            comand = "Review.destory({})".format(tstID)
            self.assertFalse(HBNBCommand().onecmd(comand))
            self.assertNotIn(obj, storage.all())


class TestHBNBCommand_all(unittest.TestCase):
    '''unittests For Testing All Of The HBNB Command Interpreter'''

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_all_invalid_class(self):
        corect = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_all_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())

    def test_all_objects_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertIn("User", output.getvalue().strip())
            self.assertIn("State", output.getvalue().strip())
            self.assertIn("Place", output.getvalue().strip())
            self.assertIn("City", output.getvalue().strip())
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertIn("Review", output.getvalue().strip())

    def test_all_single_object_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())

    def test_all_single_object_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", output.getvalue().strip())
            self.assertNotIn("User", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", output.getvalue().strip())
            self.assertNotIn("BaseModel", output.getvalue().strip())


class TestHBNBCommand_update(unittest.TestCase):
    '''unittests For Testing Update From The HBNB Command Interpreter'''

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

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

    def test_update_missing_class(self):
        corect = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_update_invalid_class(self):
        corect = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_update_missing_id_space_notation(self):
        corect = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_update_missing_id_dot_notation(self):
        corect = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update()"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update()"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_update_invalid_id_space_notation(self):
        corect = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place 1"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review 1"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_update_invalid_id_dot_notation(self):
        corect = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
            self.assertEqual(corect, output.getvalue().strip())

    def test_update_missing_attr_name_space_notation(self):
        corect = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tstId = output.getvalue().strip()
            tstCmd = "update BaseModel {}".format(tstId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tstId = output.getvalue().strip()
            tstCmd = "update User {}".format(tstId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tstId = output.getvalue().strip()
            tstCmd = "update State {}".format(tstId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tstId = output.getvalue().strip()
            tstCmd = "update City {}".format(tstId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tstId = output.getvalue().strip()
            tstCmd = "update Amenity {}".format(tstId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(correct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tstId = output.getvalue().strip()
            tstCmd = "update Place {}".format(tstId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(correct, output.getvalue().strip())

    def test_update_missing_attr_name_dot_notation(self):
        corect = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tstId = output.getvalue().strip()
            tstCmd = "BaseModel.update({})".format(tstId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tstId = output.getvalue().strip()
            tstCmd = "User.update({})".format(tstId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tstId = output.getvalue().strip()
            tstCmd = "State.update({})".format(tstId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tstId = output.getvalue().strip()
            tstCmd = "City.update({})".format(tstId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tstId = output.getvalue().strip()
            tstCmd = "Amenity.update({})".format(tstId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tstId = output.getvalue().strip()
            tstCmd = "Place.update({})".format(tstId)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())

    def test_update_missing_attr_value_space_notation(self):
        corect = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tstId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "update BaseModel {} attr_name".format(tstId)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tstId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "update User {} attr_name".format(tstId)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tstId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "update State {} attr_name".format(tstId)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tstId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "update City {} attr_name".format(tstId)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tstId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "update Amenity {} attr_name".format(tstId)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "update Place {} attr_name".format(tstId)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tstId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "update Review {} attr_name".format(tstId)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())

    def test_update_missing_attr_value_dot_notation(self):
        corect = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tstId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "BaseModel.update({}, attr_name)".format(tstId)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tstId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "User.update({}, attr_name)".format(tstId)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tstId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "State.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tstId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "City.update({}, attr_name)".format(tstId)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tstId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "Amenity.update({}, attr_name)".format(tstId)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "Place.update({}, attr_name)".format(tstId)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tstId = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmd = "Review.update({}, attr_name)".format(tstId)
            self.assertFalse(HBNBCommand().onecmd(tstCmd))
            self.assertEqual(corect, output.getvalue().strip())

    def test_update_valid_string_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tstId = output.getvalue().strip()
        tstCmd = "update BaseModel {} attr_name 'attr_value'".format(tstId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["BaseModel.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tstId = output.getvalue().strip()
        tstCmd = "update User {} attr_name 'attr_value'".format(tstId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["User.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tstId = output.getvalue().strip()
        tstCmd = "update State {} attr_name 'attr_value'".format(tstId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["State.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tstId = output.getvalue().strip()
        tstCmd = "update City {} attr_name 'attr_value'".format(tstId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["City.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstId = output.getvalue().strip()
        tstCmd = "update Place {} attr_name 'attr_value'".format(tstId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["Place.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tstId = output.getvalue().strip()
        tstCmd = "update Amenity {} attr_name 'attr_value'".format(tstId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["Amenity.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tstId = output.getvalue().strip()
        tstCmd = "update Review {} attr_name 'attr_value'".format(tstId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["Review.{}".format(tstId)].__dict__
        self.assertTrue("attr_value", tst_dct["attr_name"])

    def test_update_valid_string_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            fId = output.getvalue().strip()
        tstCmd = "BaseModel.update({}, attr_name, 'attr_value')".format(fId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["BaseModel.{}".format(fId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            fId = output.getvalue().strip()
        tstCmd = "User.update({}, attr_name, 'attr_value')".format(fId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["User.{}".format(fId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            fId = output.getvalue().strip()
        tstCmd = "State.update({}, attr_name, 'attr_value')".format(fId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["State.{}".format(fId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            fId = output.getvalue().strip()
        tstCmd = "City.update({}, attr_name, 'attr_value')".format(fId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["City.{}".format(fId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            fId = output.getvalue().strip()
        tstCmd = "Place.update({}, attr_name, 'attr_value')".format(fId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["Place.{}".format(fId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            fId = output.getvalue().strip()
        tstCmd = "Amenity.update({}, attr_name, 'attr_value')".format(fId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["Amenity.{}".format(fId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            fId = output.getvalue().strip()
        tstCmd = "Review.update({}, attr_name, 'attr_value')".format(fId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["Review.{}".format(fId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

    def test_update_valid_int_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstId = output.getvalue().strip()
        tstCmd = "update Place {} max_guest 98".format(tstId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["Place.{}".format(tstId)].__dict__
        self.assertEqual(98, tst_dct["max_guest"])

    def test_update_valid_int_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            fId = output.getvalue().strip()
        tstCmd = "Place.update({}, max_guest, 98)".format(fId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["Place.{}".format(fId)].__dict__
        self.assertEqual(98, tst_dct["max_guest"])

    def test_update_valid_float_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstId = output.getvalue().strip()
        tstCmd = "update Place {} latitude 7.2".format(tstId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["Place.{}".format(tstId)].__dict__
        self.assertEqual(7.2, tst_dct["latitude"])

    def test_update_valid_float_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            fId = output.getvalue().strip()
        tstCmd = "Place.update({}, latitude, 7.2)".format(fId)
        self.assertFalse(HBNBCommand().onecmd(tstCmd))
        tst_dct = storage.all()["Place.{}".format(fId)].__dict__
        self.assertEqual(7.2, tst_dct["latitude"])

    def test_update_valid_dictionary_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tstId = output.getvalue().strip()
        tstCmd = "update BaseModel {} ".format(tstId)
        tstCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["BaseModel.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tstId = output.getvalue().strip()
        tstCmd = "update User {} ".format(tstId)
        tstCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["User.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tstId = output.getvalue().strip()
        tstCmd = "update State {} ".format(tstId)
        tstCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["State.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tstId = output.getvalue().strip()
        tstCmd = "update City {} ".format(tstId)
        tstCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["City.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstId = output.getvalue().strip()
        tstCmd = "update Place {} ".format(tstId)
        tstCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["Place.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tstId = output.getvalue().strip()
        tstCmd = "update Amenity {} ".format(tstId)
        tstCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["Amenity.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tstId = output.getvalue().strip()
        tstCmd = "update Review {} ".format(tstId)
        tstCmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["Review.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

    def test_update_valid_dictionary_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tstId = output.getvalue().strip()
        tstCmd = "BaseModel.update({}".format(tstId)
        tstCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["BaseModel.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tstId = output.getvalue().strip()
        tstCmd = "User.update({}, ".format(tstId)
        tstCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["User.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            testId = output.getvalue().strip()
        tstCmd = "State.update({}, ".format(tstId)
        tstCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["State.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tstId = output.getvalue().strip()
        tstCmd = "City.update({}, ".format(tstId)
        tstCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["City.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")f
            testId = output.getvalue().strip()
        tstCmd = "Place.update({}, ".format(tstId)
        tstCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["Place.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tstId = output.getvalue().strip()
        tstCmd = "Amenity.update({}, ".format(tstId)
        tstCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["Amenity.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tstId = output.getvalue().strip()
        tstCmd = "Review.update({}, ".format(testId)
        tstCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["Review.{}".format(tstId)].__dict__
        self.assertEqual("attr_value", tst_dct["attr_name"])

    def test_update_valid_dictionary_with_int_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstId = output.getvalue().strip()
        tstCmd = "update Place {} ".format(tstId)
        tstCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(testCmd)
        tst_dct = storage.all()["Place.{}".format(tstId)].__dict__
        self.assertEqual(98, tst_dct["max_guest"])

    def test_update_valid_dictionary_with_int_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            testId = output.getvalue().strip()
        tstCmd = "Place.update({}, ".format(tstId)
        tstCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["Place.{}".format(tstId)].__dict__
        self.assertEqual(98, tst_dct["max_guest"])

    def test_update_valid_dictionary_with_float_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstId = output.getvalue().strip()
        tstCmd = "update Place {} ".format(tstId)
        tstCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["Place.{}".format(tstId)].__dict__
        self.assertEqual(9.8, tst_dct["latitude"])

    def test_update_valid_dictionary_with_float_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tstId = output.getvalue().strip()
        tstCmd = "Place.update({}, ".format(tstId)
        tstCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(tstCmd)
        tst_dct = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(9.8, tst_dct["latitude"])


class TestHBNBCommand_count(unittest.TestCase):
    '''unittests For Testing Count Method Of HBNB Comand Interpreter'''

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

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

    def test_count_invalid_class(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            self.assertEqual("0", output.getvalue().strip())

    def test_count_object(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            self.assertEqual("1", output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.count()"))
            self.assertEqual("1", output.getvalue().strip())


if __name__ == "__main__":
    unittest.main()

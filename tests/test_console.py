#!/usr/bin/python3
"""Defines unittests for console.py.

Unittest classes:
    TestHBNBCommand_prompting
    TestHBNBCommand_help
    TestHBNBCommand_exit
    TestHBNBCommand_create
    TestHBNBCommand_show
    TestHBNBCommand_all
    TestHBNBCommand_destroy
    TestHBNBCommand_update
"""
import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommand_prompting(unittest.TestCase):
    """Unttsts 4 tstng prmptng of d HBNB cmmnd intrprtr"""

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())


class TestHBNBCommand_help(unittest.TestCase):
    """Unttsts fr tstng hlp mssgs of d HBNB cmmnd intrprtr"""

    def test_help_quit(self):
        hg = "Quit commd 2 ext d prgrm"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(hg, output.getvalue().strip())

    def test_help_create(self):
        hg = ("Usage: create <class>\n        "
             "Create a new class instance and print its id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(hg, output.getvalue().strip())

    def test_help_EOF(self):
        hg = "EOF signal to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(hg, output.getvalue().strip())

    def test_help_show(self):
        hg = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
             "Display the string representation of a class instance of"
             " a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(hg, output.getvalue().strip())

    def test_help_destroy(self):
        hg = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n        "
             "Delete a class instance of a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(hg, output.getvalue().strip())

    def test_help_all(self):
        hg = ("Usage: all or all <class> or <class>.all()\n        "
             "Display string representations of all instances of a given class"
             ".\n        If no class is specified, displays all instantiated "
             "objcs.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(hg, output.getvalue().strip())

    def test_help_count(self):
        hg = ("Usage: count <class> or <class>.count()\n        "
             "Retrieve the number of instances of a given class.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(hg, output.getvalue().strip())

    def test_help_update(self):
        hg = ("Usage: update <class> <id> <attribute_name> <attribute_value> or"
             "\n       <class>.update(<id>, <attribute_name>, <attribute_value"
             ">) or\n       <class>.update(<id>, <dictionary>)\n        "
             "Update a class instance of a given id by adding or updating\n   "
             "     a given attribute keeyy/val pair or dictionary.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(hg, output.getvalue().strip())

    def test_help(self):
        hg = ("Documented commands (type help <topic>):\n"
             "========================================\n"
             "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(hg, output.getvalue().strip())


class TestHBNBCommand_exit(unittest.TestCase):
    """Unittests for testing exiting from the HBNB cmmd interpreter."""

    def test_quit_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommand_create(unittest.TestCase):
    """Unttsts fr tstng crt frm d HBNB cmmd intrprtr"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objcs = {}

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
        crrct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_create_invalid_class(self):
        crrct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_create_invalid_syntax(self):
        crrct = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(crrct, output.getvalue().strip())
        crrct = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_create_object(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(output.getvalue().strip()))
            tstKy = "BaseModel.{}".format(output.getvalue().strip())
            self.assertIn(tstKy, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(output.getvalue().strip()))
            tstKy = "User.{}".format(output.getvalue().strip())
            self.assertIn(tstKy, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(output.getvalue().strip()))
            tstKy = "State.{}".format(output.getvalue().strip())
            self.assertIn(tstKy, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(output.getvalue().strip()))
            tstKy = "City.{}".format(output.getvalue().strip())
            self.assertIn(tstKy, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(output.getvalue().strip()))
            tstKy = "Amenity.{}".format(output.getvalue().strip())
            self.assertIn(tstKy, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(output.getvalue().strip()))
            tstKy = "Place.{}".format(output.getvalue().strip())
            self.assertIn(tstKy, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(output.getvalue().strip()))
            tstKy = "Review.{}".format(output.getvalue().strip())
            self.assertIn(tstKy, storage.all().keys())


class TestHBNBCommand_show(unittest.TestCase):
    """Unttsts 4 tstng shw frm d HBNB cmmd intrprtr"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objcs = {}

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
        crrct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_show_invalid_class(self):
        crrct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_show_missing_id_space_notation(self):
        crrct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_show_missing_id_dot_notation(self):
        crrct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_show_no_instance_found_space_notation(self):
        crrct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show User 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show State 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Place 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("show Review 1"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_show_no_instance_found_dot_notation(self):
        crrct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.show(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.show(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.show(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["BaseModel.{}".format(tst24ID)]
            cmmd = "show BaseModel {}".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertEqual(objc24.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["User.{}".format(tst24ID)]
            cmmd = "show User {}".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertEqual(objc24.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["State.{}".format(tst24ID)]
            cmmd = "show State {}".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertEqual(objc24.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["Place.{}".format(tst24ID)]
            cmmd = "show Place {}".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertEqual(objc24.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["City.{}".format(tst24ID)]
            cmmd = "show City {}".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertEqual(objc24.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["Amenity.{}".format(tst24ID)]
            cmmd = "show Amenity {}".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertEqual(objc24.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["Review.{}".format(tst24ID)]
            cmmd = "show Review {}".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertEqual(objc24.__str__(), output.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["BaseModel.{}".format(tst24ID)]
            cmmd = "BaseModel.show({})".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertEqual(objc24.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["User.{}".format(tst24ID)]
            cmmd = "User.show({})".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertEqual(objc24.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["State.{}".format(tst24ID)]
            cmmd = "State.show({})".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertEqual(objc24.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["Place.{}".format(tst24ID)]
            cmmd = "Place.show({})".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertEqual(objc24.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["City.{}".format(tst24ID)]
            cmmd = "City.show({})".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertEqual(objc24.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["Amenity.{}".format(tst24ID)]
            cmmd = "Amenity.show({})".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertEqual(objc24.__str__(), output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["Review.{}".format(tst24ID)]
            cmmd = "Review.show({})".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertEqual(objc24.__str__(), output.getvalue().strip())


class TestHBNBCommand_destroy(unittest.TestCase):
    """Unittests for testing destroy from the HBNB cmmd interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objcs = {}

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
        crrct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_destroy_invalid_class(self):
        crrct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_destroy_id_missing_space_notation(self):
        crrct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_destroy_id_missing_dot_notation(self):
        crrct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_destroy_invalid_id_space_notation(self):
        crrct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy User 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy State 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy City 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_destroy_invalid_id_dot_notation(self):
        crrct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_destroy_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["BaseModel.{}".format(tst24ID)]
            cmmd = "destroy BaseModel {}".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertNotIn(objc24, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["User.{}".format(tst24ID)]
            cmmd = "show User {}".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertNotIn(objc24, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["State.{}".format(tst24ID)]
            cmmd = "show State {}".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertNotIn(objc24, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["Place.{}".format(tst24ID)]
            cmmd = "show Place {}".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertNotIn(objc24, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["City.{}".format(tst24ID)]
            cmmd = "show City {}".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertNotIn(objc24, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["Amenity.{}".format(tst24ID)]
            cmmd = "show Amenity {}".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertNotIn(objc24, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["Review.{}".format(tst24ID)]
            cmmd = "show Review {}".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertNotIn(objc24, storage.all())

    def test_destroy_objects_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["BaseModel.{}".format(tst24ID)]
            cmmd = "BaseModel.destroy({})".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertNotIn(objc24, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["User.{}".format(tst24ID)]
            cmmd = "User.destroy({})".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertNotIn(objc24, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["State.{}".format(tst24ID)]
            cmmd = "State.destroy({})".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertNotIn(objc24, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["Place.{}".format(tst24ID)]
            cmmd = "Place.destroy({})".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertNotIn(objc24, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["City.{}".format(tst24ID)]
            cmmd = "City.destroy({})".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertNotIn(objc24, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["Amenity.{}".format(tst24ID)]
            cmmd = "Amenity.destroy({})".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertNotIn(objc24, storage.all())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            objc24 = storage.all()["Review.{}".format(tst24ID)]
            cmmd = "Review.destory({})".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(cmmd))
            self.assertNotIn(objc24, storage.all())


class TestHBNBCommand_all(unittest.TestCase):
    """Unittests for testing all of the HBNB cmmd interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objcs = {}

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
        crrct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            self.assertEqual(crrct, output.getvalue().strip())

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
    """Unittests for testing update from the HBNB cmmd interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objcs = {}

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
        crrct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_update_invalid_class(self):
        crrct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_update_missing_id_space_notation(self):
        crrct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_update_missing_id_dot_notation(self):
        crrct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update()"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update()"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_update_invalid_id_space_notation(self):
        crrct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update User 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update State 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update City 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Place 1"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("update Review 1"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_update_invalid_id_dot_notation(self):
        crrct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("User.update(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("State.update(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("City.update(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_update_missing_attr_name_space_notation(self):
        crrct = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tst24ID = output.getvalue().strip()
            tstCmmd = "update BaseModel {}".format(tst24ID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tst24ID = output.getvalue().strip()
            tstCmmd = "update User {}".format(tst24ID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tst24ID = output.getvalue().strip()
            tstCmmd = "update State {}".format(tst24ID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tst24ID = output.getvalue().strip()
            tstCmmd = "update City {}".format(tst24ID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tst24ID = output.getvalue().strip()
            tstCmmd = "update Amenity {}".format(tst24ID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tst24ID = output.getvalue().strip()
            tstCmmd = "update Place {}".format(tst24ID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_update_missing_attr_name_dot_notation(self):
        crrct = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            tst24ID = output.getvalue().strip()
            tstCmmd = "BaseModel.update({})".format(tst24ID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            tst24ID = output.getvalue().strip()
            tstCmmd = "User.update({})".format(tst24ID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            tst24ID = output.getvalue().strip()
            tstCmmd = "State.update({})".format(tst24ID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            tst24ID = output.getvalue().strip()
            tstCmmd = "City.update({})".format(tst24ID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            tst24ID = output.getvalue().strip()
            tstCmmd = "Amenity.update({})".format(tst24ID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            tst24ID = output.getvalue().strip()
            tstCmmd = "Place.update({})".format(tst24ID)
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_update_missing_attr_value_space_notation(self):
        crrct = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmmd = "update BaseModel {} attr_name".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmmd = "update User {} attr_name".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmmd = "update State {} attr_name".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmmd = "update City {} attr_name".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmmd = "update Amenity {} attr_name".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmmd = "update Place {} attr_name".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmmd = "update Review {} attr_name".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_update_missing_attr_value_dot_notation(self):
        crrct = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmmd = "BaseModel.update({}, attr_name)".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmmd = "User.update({}, attr_name)".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmmd = "State.update({}, attr_name)".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmmd = "City.update({}, attr_name)".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmmd = "Amenity.update({}, attr_name)".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmmd = "Place.update({}, attr_name)".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tst24ID = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            tstCmmd = "Review.update({}, attr_name)".format(tst24ID)
            self.assertFalse(HBNBCommand().onecmd(tstCmmd))
            self.assertEqual(crrct, output.getvalue().strip())

    def test_update_valid_string_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update BaseModel {} attr_name 'attr_value'".format(tst24ID)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["BaseModel.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update User {} attr_name 'attr_value'".format(tst24ID)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["User.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update State {} attr_name 'attr_value'".format(tst24ID)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["State.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update City {} attr_name 'attr_value'".format(tst24ID)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["City.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update Place {} attr_name 'attr_value'".format(tst24ID)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["Place.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update Amenity {} attr_name 'attr_value'".format(tst24ID)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["Amenity.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update Review {} attr_name 'attr_value'".format(tst24ID)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["Review.{}".format(tst24ID)].__dict__
        self.assertTrue("attr_value", tst_dictio["attr_name"])

    def test_update_valid_string_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tId24 = output.getvalue().strip()
        tstCmmd = "BaseModel.update({}, attr_name, 'attr_value')".format(tId24)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["BaseModel.{}".format(tId24)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tId24 = output.getvalue().strip()
        tstCmmd = "User.update({}, attr_name, 'attr_value')".format(tId24)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["User.{}".format(tId24)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tId24 = output.getvalue().strip()
        tstCmmd = "State.update({}, attr_name, 'attr_value')".format(tId24)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["State.{}".format(tId24)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tId24 = output.getvalue().strip()
        tstCmmd = "City.update({}, attr_name, 'attr_value')".format(tId24)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["City.{}".format(tId24)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId24 = output.getvalue().strip()
        tstCmmd = "Place.update({}, attr_name, 'attr_value')".format(tId24)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["Place.{}".format(tId24)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tId24 = output.getvalue().strip()
        tstCmmd = "Amenity.update({}, attr_name, 'attr_value')".format(tId24)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["Amenity.{}".format(tId24)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tId24 = output.getvalue().strip()
        tstCmmd = "Review.update({}, attr_name, 'attr_value')".format(tId24)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["Review.{}".format(tId24)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

    def test_update_valid_int_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update Place {} max_guest 98".format(tst24ID)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["Place.{}".format(tst24ID)].__dict__
        self.assertEqual(98, tst_dictio["max_guest"])

    def test_update_valid_int_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId24 = output.getvalue().strip()
        tstCmmd = "Place.update({}, max_guest, 98)".format(tId24)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["Place.{}".format(tId24)].__dict__
        self.assertEqual(98, tst_dictio["max_guest"])

    def test_update_valid_float_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update Place {} latitude 7.2".format(tst24ID)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["Place.{}".format(tst24ID)].__dict__
        self.assertEqual(7.2, tst_dictio["latitude"])

    def test_update_valid_float_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tId24 = output.getvalue().strip()
        tstCmmd = "Place.update({}, latitude, 7.2)".format(tId24)
        self.assertFalse(HBNBCommand().onecmd(tstCmmd))
        tst_dictio = storage.all()["Place.{}".format(tId24)].__dict__
        self.assertEqual(7.2, tst_dictio["latitude"])

    def test_update_valid_dictionary_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update BaseModel {} ".format(tst24ID)
        tstCmmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["BaseModel.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update User {} ".format(tst24ID)
        tstCmmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["User.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update State {} ".format(tst24ID)
        tstCmmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["State.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update City {} ".format(tst24ID)
        tstCmmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["City.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update Place {} ".format(tst24ID)
        tstCmmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["Place.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update Amenity {} ".format(tst24ID)
        tstCmmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["Amenity.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update Review {} ".format(tst24ID)
        tstCmmd += "{'attr_name': 'attr_value'}"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["Review.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

    def test_update_valid_dictionary_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
            tst24ID = output.getvalue().strip()
        tstCmmd = "BaseModel.update({}".format(tst24ID)
        tstCmmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["BaseModel.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create User")
            tst24ID = output.getvalue().strip()
        tstCmmd = "User.update({}, ".format(tst24ID)
        tstCmmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["User.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create State")
            tst24ID = output.getvalue().strip()
        tstCmmd = "State.update({}, ".format(tst24ID)
        tstCmmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["State.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create City")
            tst24ID = output.getvalue().strip()
        tstCmmd = "City.update({}, ".format(tst24ID)
        tstCmmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["City.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tst24ID = output.getvalue().strip()
        tstCmmd = "Place.update({}, ".format(tst24ID)
        tstCmmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["Place.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Amenity")
            tst24ID = output.getvalue().strip()
        tstCmmd = "Amenity.update({}, ".format(tst24ID)
        tstCmmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["Amenity.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Review")
            tst24ID = output.getvalue().strip()
        tstCmmd = "Review.update({}, ".format(tst24ID)
        tstCmmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["Review.{}".format(tst24ID)].__dict__
        self.assertEqual("attr_value", tst_dictio["attr_name"])

    def test_update_valid_dictionary_with_int_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update Place {} ".format(tst24ID)
        tstCmmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["Place.{}".format(tst24ID)].__dict__
        self.assertEqual(98, tst_dictio["max_guest"])

    def test_update_valid_dictionary_with_int_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tst24ID = output.getvalue().strip()
        tstCmmd = "Place.update({}, ".format(tst24ID)
        tstCmmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["Place.{}".format(tst24ID)].__dict__
        self.assertEqual(98, tst_dictio["max_guest"])

    def test_update_valid_dictionary_with_float_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tst24ID = output.getvalue().strip()
        tstCmmd = "update Place {} ".format(tst24ID)
        tstCmmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["Place.{}".format(tst24ID)].__dict__
        self.assertEqual(9.8, tst_dictio["latitude"])

    def test_update_valid_dictionary_with_float_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as output:
            HBNBCommand().onecmd("create Place")
            tst24ID = output.getvalue().strip()
        tstCmmd = "Place.update({}, ".format(tst24ID)
        tstCmmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(tstCmmd)
        tst_dictio = storage.all()["Place.{}".format(tst24ID)].__dict__
        self.assertEqual(9.8, tst_dictio["latitude"])


class TestHBNBCommand_count(unittest.TestCase):
    """Unittests for testing count method of HBNB comand interpreter."""

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


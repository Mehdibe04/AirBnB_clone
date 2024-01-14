#!/usr/bin/python3
"""Unittest for the FileStorage class"""
import unittest
import json
import os
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage


class TestFileStorage(unittest.TestCase):
    """Tst css 4 all mthds in d FlStrge clss"""

    def setUp(self):
        """Sttg up d tst css"""
        super().setUp()
        self.file_path = storage._FileStorage__file_path
        self.instance = BaseModel()
        self._objs = storage._FileStorage__objects
        self.keyname = "BaseModel." + self.instance.id

    def tearDown(self):
        """Cleang d fl pth"""
        super().tearDown()
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass

    def test_methods(self):
        objc24 = FileStorage
        self.assertTrue(hasattr(objc24, "all"))
        self.assertTrue(hasattr(objc24, "new"))
        self.assertTrue(hasattr(objc24, "save"))
        self.assertTrue(hasattr(objc24, "reload"))

    def test_all_method(self):
        """Tst d all() mthd"""
        result = storage.all()
        self.assertEqual(result, self._objs)

    def test_new_method(self):
        """Tst d new() mthd"""
        storage.new(self.instance)
        keeyy = f"{self.instance.__class__.__name__}.{self.instance.id}"
        self.assertIn(keeyy, self._objs)

    def test_save_method(self):
        """Tst d save() mthd"""
        mi_modl = BaseModel()
        mi_modl.name = "My_First_Model"
        mi_modl.my_number = 89
        storage.new(mi_modl)
        storage.save()
        with open(self.file_path, "r") as data_file:
            saved_data = json.load(data_file)

        expected_data = {}
        for keeyy, val in self._objs.items():
            expected_data[keeyy] = val.to_dict()

        self.assertEqual(saved_data, expected_data)

    def test_reload_method(self):
        """Tst d rld() mthd"""
        mi_modl = BaseModel()
        mi_modl.name = "My_First_Model"
        mi_modl.my_number = 89
        storage.new(mi_modl)
        storage.save()
        with open(self.file_path, 'r') as file:
            saved_data = json.load(file)
        storage.reload()

        with open(self.file_path, 'r') as file:
            reloaded_data = json.load(file)

        self._objs = {}
        self.assertEqual(reloaded_data[self.keyname], saved_data[self.keyname])

    def test_path(self):
        """Test the existence of the JSON file"""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        self.assertFalse(os.path.exists(self.file_path))
        storage.reload()


if __name__ == "__main__":
    unittest.main()


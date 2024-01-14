#!/usr/bin/python3
"""Unittest for the BaseModel Class """
import datetime
from models.base_model import BaseModel
import os
import json
import unittest


class TestBaseModel(unittest.TestCase):
    """
    This class contains unittests for the BaseModel class.
    """
    def setUp(self):
        """Method that the setUp the cases to test"""
        self.my_model = BaseModel()
        self.my_model.name = "My_First_Model"
        self.my_model.my_number = 89
        self.id = self.my_model.id
        self.type_1 = datetime.datetime
        self.my_model_json = self.my_model.to_dict()

    def tearDown(self):
        """Method to clean the tests"""
        del self.my_model

    def test_init_(self):
        """Test for The __init__ method in the BaseModel"""
        self.assertIsInstance(self.my_model, BaseModel)

    def test_new_attribue(self):
        """Test for the saving attributes"""
        self.assertEqual(self.my_model.name, "My_First_Model")
        self.assertEqual(self.my_model.my_number, 89)

    def test_id(self):
        """Test for the id generating"""
        self.assertEqual(self.id, self.my_model.id)

    def test_id_unique(self):
        """
        Test if each instance of BaseModel has a unique id.
        """
        b_mdl1 = BaseModel()
        b_mdl2 = BaseModel()
        self.assertNotEqual(b_mdl1.id, b_mdl2.id)

    def test_str_representation(self):
        """
        Test the __str__ method of BaseModel.
        """
        base_model = BaseModel()
        strg_rep = str(base_model)
        self.assertIn("[BaseModel]", strg_rep)
        self.assertIn(base_model.id, strg_rep)
        self.assertIn(str(base_model.__dict__), strg_rep)

    def test_created_at(self):
        """Tst 4 d type of crted_at"""
        self.assertEqual(self.type_1, type(self.my_model.created_at))

    def test_to_dict_created_at_isoformat(self):
        self.assertEqual(self.my_model_json['created_at'],
                         self.my_model.created_at.isoformat())

    def test_to_dict_updated_at_isoformat(self):
        self.assertEqual(self.my_model_json['updated_at'],
                         self.my_model.updated_at.isoformat())

    def test_save_updates_updated_at(self):
        prev_updated_at = self.my_model.updated_at
        self.my_model.save()
        self.assertNotEqual(prev_updated_at, self.my_model.updated_at)

    def test_to_dict(self):
        """Test for to_dic method"""
        self.assertEqual(self.my_model_json, self.my_model.to_dict())

    def test_to_dict_contains_correct_keys(self):
        keeyys = ['id', 'created_at', 'updated_at', '__class__']
        for keeyy in keeyys:
            self.assertIn(keeyy, self.my_model_json)

    def test_to_dict_returns(self):
        """
        Tst if to_dict mthd rtrns a
        dictio wth d crrct attrbts
        """
        base_model = BaseModel()
        base_model_dict = base_model.to_dict()
        self.assertIsInstance(base_model_dict, dict)
        self.assertIn("__class__", base_model_dict)
        self.assertEqual(base_model_dict["__class__"], "BaseModel")
        self.assertIn("id", base_model_dict)
        self.assertIn("created_at", base_model_dict)
        self.assertIn("updated_at", base_model_dict)


if __name__ == '__main__':
    unittest.main()


#!/usr/bin/python3
"""Mdl fr FlStrge clss"""
import datetime
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:

    """Clss fr strg & retrvg data"""
    __f_pth = "file_object.json"
    __objcs = {}

    def all(self, model_type=None):
        """Rtrns d dictio __objcs
        or objcts of a spcfc mdl type"""
        if model_type:
            objcs = {
                keeyy: objc24
                for keeyy, objc24 in FileStorage.__objcs.items()
                if isinstance(objc24, self.classes().get(model_type))
            }
            return [str(objc24) for objc24 in objcs.values()]
        return FileStorage.__objcs

    def new(self, objc24):
        """sets iin __objcs d objc24 wth keeyy <objc24 class name>.id"""
        keeyy = f"{type(objc24).__name__}.{objc24.id}"
        FileStorage.__objcs[keeyy] = objc24

    def save(self):
        """ serializes __objcs to the JSON file (path: __f_pth)"""
        with open(FileStorage.__f_pth, "w", encoding="utf-8") as file:
            dictio_t = {
                kl: w.to_dict()
                for kl, w in FileStorage.__objcs.items()
                }
            json.dump(dictio_t, file)

    def delete(self, objc24):
        """Dlts objc frm __objcs if it exsts"""
        del FileStorage.__objcs[objc24]
        self.save()

    def classes(self):
        """Rtrns a dictio of vld clsss & thr rfrcs"""

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
            }
        return classes

    def reload(self):
        """Rlds d strd objcs"""
        if not os.path.isfile(FileStorage.__f_pth):
            return
        with open(FileStorage.__f_pth, "r", encoding="utf-8") as file:
            objc_dictio = json.load(file)
            objc_dictio = {kl: self.classes()[w["__class__"]](**w)
                        for kl, w in objc_dictio.items()}
            FileStorage.__objcs = objc_dictio

    def attributes(self):
        """Rtrns d vld attrbts & thr tps fr clssnm"""
        attributes = {
                "BaseModel": {
                    "id": str,
                    "created_at": datetime.datetime,
                    "updated_at": datetime.datetime
                    },

                "User": {
                    "email": str,
                    "password": str,
                    "first_name": str,
                    "last_name": str
                    },

                "State": {
                    "name": str
                    },

                "City": {
                    "state_id": str,
                    "name": str
                    },

                "Amenity": {
                    "name": str
                    },

                "Place": {
                    "city_id": str,
                    "user_id": str,
                    "name": str,
                    "description": str,
                    "number_rooms": int,
                    "number_bathrooms": int,
                    "max_guest": int,
                    "price_by_night": int,
                    "latitude": float,
                    "longitude": float,
                    "amenity_ids": list
                    },

                "Review": {
                    "place_id": str,
                    "user_id": str,
                    "text": str
                    }
                }
        return attributes


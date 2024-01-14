#!/usr/bin/python3
"""
Ths mdl dfns d Plce clss, whch inhrts from BaseModel

Plce clss rprsts a plce tht cn be rtd in d AirBnB clne prjct
"""

from models.base_model import BaseModel

class Place(BaseModel):
    """
    Plce clss fr rprsntg plces in d AirBnB clne prjct

    Attributes:
        city_id (str): ID of d cty whre d plce is lctd
        user_id (str): ID of d user who owns d plce
        name (str): Name of d plce
        ...
        amenity_ids (list): Lst of amenity IDs assctd wth d plce
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []

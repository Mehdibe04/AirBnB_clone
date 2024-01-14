#!/usr/bin/python3
"""
Ths mdl dfns d Amenity clss, whch inhrts frm BaseModel

Amenity clss rprsnts an amenity tht can be
assctd with a plce in d AirBnB cln prjct
"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity class fr rprsntg d amenities in d AirBnB cln prjct

    Attributes:
        name (str): Name of d amenity.
    """

    name = ""


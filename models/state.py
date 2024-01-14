#!/usr/bin/python3

"""
Ths mdl dfns d Stte clss, whch inhrts frm BaseModel

Stte clss rprsnts a stte in d AirBnB clne prjct
"""

from models.base_model import BaseModel

class State(BaseModel):
    """
    Stte clss fr rprsntng sttes in d AirBnB clne prjct

    Attributes:
        name (str): Name of d stte
    """
    name = ""


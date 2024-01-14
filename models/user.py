#!/usr/bin/python3
"""
Ths mdle dfns d Usr clss, whch inhrts from BaseModel

User clss rprsnts a usr in d AirBnB clne prjct
"""

from models.base_model import BaseModel

class User(BaseModel):
    """
    d Usr clss inhrts frm BaseModel &
    dfns attrbts/mthds spcfc 2 Usr objcs
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""


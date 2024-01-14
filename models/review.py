#!/usr/bin/python3
"""
Ths mdle dfns d Rvw clss, whch inhrts from BaseModel
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    Rvw clss fr rprsntg rvws
    of plcs in d AirBnB clne prjct

    Attributes:
        place_id (str): ID of d plce bng rvwd
        user_id (str): ID of d user who wrte d rvw
        text (str): d rvw txt
    """
    place_id = ""
    user_id = ""
    text = ""


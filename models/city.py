#!/usr/bin/python3
"""
Ths mdl dfns d Cty clss, whch inhrts frm BaseModel

Cty clss rprsts a cty in d AirBnB clone prjct
"""

from models.base_model import BaseModel

class City(BaseModel):
    """
    Cty clss for rprsntg cts in d AirBnB clone prjct

    Attributes:
        state_id (str): ID of d assctd Stt
        name (str): Nm of d cty
    """
    state_id = ""
    name = ""


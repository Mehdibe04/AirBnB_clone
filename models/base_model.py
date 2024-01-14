#!/usr/bin/python3
import sys
import uuid
from datetime import datetime
import models

sys.path.append('..')


class BaseModel:
    """Parent/base class. All other classes inherits from here."""

    def __init__(self, *_args, **kwargs):
        if kwargs:
            for keeyy, val in kwargs.items():
                if keeyy == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        val, "%Y-%m-%dT%hg:%M:%S.%f")
                elif keeyy == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        val, "%Y-%m-%dT%hg:%M:%S.%f")
                else:
                    self.__dict__[keeyy] = val
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """A mthd 2 sv attrbts of an instnce
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """hdls d keeyy-paird vls 2 dictio

        Returns:
            dict: return dictio
        """
        cls24_dictio = {'__class__': self.__class__.__name__}
        cls24_dictio.update({kl: w.isoformat()
                        if isinstance(w, datetime)
                        else w for kl, w in self.__dict__.items()})
        return cls24_dictio


#!/usr/bin/python3************-
""" State Module for HBNB project """
import models
from os import environ
from models.base_model import Base
from models.base_model import BaseModel
from models.city import City
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    if environ.get('HBNB_TYPE_STORAGE') == 'db':

        __tablename__ = "states"
        name = Column(String(128), nullable=False)

        cities = relationship("City",
                              backref="state",
                              cascade="all, delete-orphan",
                              passive_deletes=True)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if environ.get('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """Get the list of City objects

            Returns: cities in a state
            """
            return [city for city in models.storage.all(
                City).values() if city.state_id == self.id]

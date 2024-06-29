#!/usr/bin/python3
""" Place Module for HBNB project """
from os import environ
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
import models
from models.amenity import Amenity
from models.base_model import Base, BaseModel


if environ.get('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id', ondelete='CASCADE'),
                                 primary_key=True,
                                 nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id',
                                            ondelete='CASCADE'),
                                 primary_key=True,
                                 nullable=False))


class Place(BaseModel, Base):
    """
    Define a place

    Attributes:
        __tablename__ (str): Place MySQL table name

        city_id (str): city id
        user_id (str): user id
        name (str): name of Place.
        description (str): describe place
        number_rooms (int): number of rooms
        number_bathrooms (int): number of bathrooms
        max_guest (int): max number of guests allowed
        price_by_night (int): price of room per night
        latitude (float): latitude of place
        longitude (float): longitude of place
        amenity_ids (list (of st)): list of Amenity.id of place.
    """

    if environ.get('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "places"

        city_id = Column(String(60), ForeignKey("cities.id",
                         ondelete='CASCADE'), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id",
                         ondelete='CASCADE'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship('Review', backref='place',
                               cascade='all, delete-orphan',
                               passive_deletes=True)
        amenities = relationship('Amenity', backref='place_amenities',
                                 cascade='all, delete',
                                 secondary=place_amenity,
                                 viewonly=False,
                                 passive_deletes=True)

    else:
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

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)

    if environ.get('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """Returns the list of Review instance

            Returns:
                list: a list of reviews
            """
            from models.review import Review
            return [review for review in models.storage.all(Review).values()
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """Returns the list of Amenity instance
            Returns:
                list: list of amenity instances
            """
            return [amenity for amenity in models.storage.all(Amenity).values()
                    if amenity.place_id == self.id]

        @amenities.setter
        def amenities(self, obj):
            """append method for adding an Amenity.id to the attribute
            amenity_ids. This method should accept only Amenity object,/ NULL.
            """
            if not isinstance(obj, Amenity):
                return
            self.amenity_ids.append(obj.id)

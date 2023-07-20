#!/usr/bin/python3
""" Place Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
import models
from os import getenv


"""An intermediary table that maps(many-many) the relationships between
the Place and Amenity classes"""

place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    if getenv("HBNB_TYPE_STORAGE", "fs") == "db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True, default=0)
        longitude = Column(Float, nullable=True, default=0)
        amenity_ids = []
        reviews = relationship(
                "Review", cascade="all, delete, delete-orphan",
                backref="place")
        amenities = relationship(
                'Amenity', secondary=place_amenity, viewonly=False,
                back_populates="place_amenities")
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

    @property
    def reviews(self):
        """It returns the list of review instances with place_id equals to
        the current Place.id. This is the FileStorage way of creating
        relationshipbetween Place and Review.
        """
        review_list = []
        obj_store = models.storage.all("Review").values()

        for review in obj_store:
            if review.state_id == self.id:
                review_list.append(review)
        return review_list

        @property
        def amenities(self):
            '''
                Return list: amenity inst's if Amenity.place_id=curr place.id
                FileStorage many to many relationship between Place and Amenity
            '''
            list_amenities = []
            for amenity in models.storage.all(Amenity).values():
                if amenity.place_id == self.id:
                    amenity_list.append(amenity)
            return list_amenities

        @amenities.setter
        def amenities(self, amenity=None):
            '''
                Set list: amenity instances if Amenity.place_id==curr place.id
                Set by adding instance objs to amenity_ids attribute in Place
            '''
            if amenity:
                for amenity in models.storage.all(Amenity).values():
                    if amenity.place_id == self.id:
                        amenity_ids.append(amenity)

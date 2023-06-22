#!/usr/bin/python3
""" Place Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
import models


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

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
            "Review", cascade="all, delete, delete-orphan", backref="place")

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

#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import models
from os import getenv


class City(BaseModel, Base):
    """ The city class, contains state ID and name """

    __tablename__ = 'cities'

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        """Map many instances of class Places to single class City
        (1 - many relationship) also create the attribute cities in class
        Place for easy access of city Object from Place
        """
        places = relationship(
                "Place", cascade="all, delete, delete-orphan", backref='city')
    else:
        state_id = ""
        name = ""

#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
import models
from models.city import City
from os import getenv


class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        """Establish a 1-many relationship with the class City and create
        an attribute called state in class City so the State obj can be
        accessed from the City objects
        the cascade tells what happens when State class is modified or deleted
        In this case, once state is deleted, all City objs are deleted.
        Once a city obj is dissociated from State, it is deleted
        """
        cities = relationship(
                'City', cascade='all, delete, delete-orphan', backref='state')
    else:
        name = ""

    @property
    def cities(self):
        """It returns the list of City instances with state_id equals to
        the current State.id. This is the FileStorage way of creating
        relationshipbetween State and City.
        """
        city_list = []
        obj_store = models.storage.all(City).values()

        for city in obj_store:
            if city.state_id == self.id:
                city_list.append(city)
        return city_list

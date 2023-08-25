#!/usr/bin/python3
"""This module defines the engine for the MySQL database"""

from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import models


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Contructor for the class DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB"),
                                             pool_pre_ping=True))

        if getenv("HBNB_ENV ") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Method to return a dictionary of objects"""
        if not cls:
            data_list = self.__session.query(Amenity)
            data_list.extend(self.__session.query(City))
            data_list.extend(self.__session.query(Place))
            data_list.extend(self.__session.query(Review))
            data_list.extend(self.__session.query(State))
            data_list.extend(self.__session.query(User))
        else:
            data_list = self.__session.query(cls)
        return {'{}.{}'.format(type(obj).__name__, obj.id): obj
                for obj in data_list}

    def new(self, obj):
        """Method to add a new object to the current database"""
        self.__session.add(obj)

    def save(self):
        """Method to commit all changes to the current database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Method to delete a new object to the current database"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Method to create the current database session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """public methodto to call remove method"""
        self.__session.close()

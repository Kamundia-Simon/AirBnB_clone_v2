#!/usr/bin/python3
"""Defines the DBStorage eng"""
import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.amenity import Amenity
from models.base_model import Base, BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """REp database storage egine
    attributeibutes:
        __file_path: path to the JSON file
        __objects: objects stored
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes new instances of DBStorage.
        """
        try:
            user = os.environ.get('HBNB_MYSQL_USER')
            password = os.environ.get('HBNB_MYSQL_PWD')
            host = os.environ.get('HBNB_MYSQL_HOST')
            db = os.environ.get('HBNB_MYSQL_DB')
            env = os.environ.get('HBNB_ENV')
            attributes = [user, password, host, db]
            for attribute in attributes:
                if attribute is None:
                    print("Missing attributes env var")

            conn_str = "mysql+mysqldb://{}:{}@{}/{}".format(
                        user, password, host, db)
            # create engine and session
            self.__engine = create_engine(conn_str, pool_pre_ping=True)

            # drop all tables in DB
            if env == 'test':
                Base.metadata.drop_all(bind=self.__engine, checkfirst=True)
        except Exception as e:
            print("raised exception in init")
            print(e)

    def all(self, cls=None):
        """query on the current db

        key = <class-name>.<object-id>
        value = object

        Args:
            cls : class

        Returns:
            dict: al objects
        """
        new_dict = {}
        for c in classes:
            if cls is None or cls is classes[c] or cls is c:
                objs = self.__session.query(classes[c]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """adds the object to the current database session

        Args:
            obj: given object
        """
        if obj and self.__session:
            self.__session.add(obj)

    def save(self):
        """commits all changes of the current database sessio
        """
        if self.__session:
            self.__session.commit()

    def delete(self, obj=None):
        """deletes obj if not none from the session
        """
        try:
            self.__session.delete(obj)
        except Exception:
            pass

    def reload(self):
        """creates all tables in database
        """
        try:
            Base.metadata.create_all(self.__engine)
            session_factory = sessionmaker(bind=self.__engine,
                                           expire_on_commit=False)
            self.__session = scoped_session(session_factory)
        except Exception as E:
            print(E)

    def close(self):
        """removes our session"""
        self.__session.remove()

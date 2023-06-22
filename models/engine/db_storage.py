#!/usr/bin/python3

"""The new database engine"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel
from models.state import State
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """New storage class for connecting classes to database"""

    __engine = None
    __session = None

    def __init__(self):
        """Create connection to mysql server immediately an
        instance of the class is created"""

        user = getenv("HBNB_MYSQL_USER")
        pswrd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        """Establish connection to database"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            user, pswrd, host, db), pool_pre_ping=True)

        """Delete all tables created in database if condition is met"""
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session. This is
        main done so we can see the output of the other functions effect
        like new(), save() e.t.c on the database from the terminal"""

        dic = {}
        if cls:
            if isinstance(str, cls):
                cls = eval(cls)
            objects = self.__session.query(cls).all()
            for obj in objects:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                dic[key] = obj
        else:
            #valid_classes = [State, City, User, Place, Review, Amenity]
            valid_classes = [State, City, User, Place, Review]
            for clss in valid_classes:
                objects = self.__session.query(clss).all()
                if len(objects) > 0:
                    for obj in objects:
                        key = "{}.{}".format(obj.__class__.__name__, obj.id)
                        dic[key] = obj
        return (dic)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database (feature of SQLAlchemy)
        (WARNING: all classes who inherit from Base must be imported
        before calling Base.metadata.create_all(engine))
        """
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        """Session used to interact with the database to make queries"""
        self.__session = Session()

    def close(self):
        """Remove private session attribute"""
        self.__session.close()

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    Date,
    Point,
    Boolean
)

from .meta import Base


class Language(Base):
    __tablename__ = 'programming_language'
    id = Column(Integer, primary_key=True)
    version_id = Column(Integer, foreign_key = True)
    name = Column(Unicode)

class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, foreign_key=True)
    name = Column(Unicode)
    long_lat = Column(Point)

class Employer(Base):
    __tablename__ = 'employer'
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, foreign_key=True)
    name = Column(Unicode)
    reputation = Column(Integer)

class Website(Base):
    __tablename__ = 'website'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    url = Column(Unicode)
    refresh_rate = Column(Integer)
    friendly = Column(Boolean)
    has_api = Column(Boolean)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    firstname = Column(Unicode)
    lastname = Column(Unicode)
    email = Column(Unicode)
    passphrase = Column(Unicode)
    last_seen = Column(Date)
    favorites = Column(Blob)
    csv = Column(Blob)

class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    version_id = Column(Integer, foreign_key=True)
    city_id = Column(Integer, foreign_key=True)
    employer_id = Column(Integer, foreign_key=True)
    source_id = Column(Integer, foreign_key=True)
    currency_id = Column(Integer, foreign_key=True)
    language_id = Column(Integer, foreign_key=True)
    creation_date = Column(Date)
    update_date = Column(Date)
    tile = Column(Integer)
    description = Column(Integer)
    salary = Column(Integer)
    sponsors_visa = Column(Boolean)
    url = Column(Unicode)
    skills = Column(PickleType)


Index('index', Job.title, unique=True, mysql_length=255)

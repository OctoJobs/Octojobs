from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    Date,
    Point,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .meta import Base

Base = declarative_base

class Language(Base):
    __tablename__ = 'programming_language'
    id = Column(Integer, primary_key=True)
    job = relationship("Job", back_populates="parent")
    name = Column(Unicode)

class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    job = relationship("Job", back_populates="parent")
    country_id = Column(Integer, foreign_key=True)
    name = Column(Unicode)
    long_lat = Column(Point)

class Employer(Base):
    __tablename__ = 'employer'
    id = Column(Integer, primary_key=True)
    job = relationship("Job", back_populates="parent")
    city_id = Column(Integer, foreign_key=True)
    name = Column(Unicode)
    reputation = Column(Integer)

class Website(Base):
    __tablename__ = 'website'
    id = Column(Integer, primary_key=True)
    job = relationship("Job", back_populates="parent")
    name = Column(Unicode)
    url = Column(Unicode)
    refresh_rate = Column(Integer)
    friendly = Column(Boolean)
    has_api = Column(Boolean)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    job = relationship("Job", back_populates="parent")
    firstname = Column(Unicode)
    lastname = Column(Unicode)
    email = Column(Unicode)
    passphrase = Column(Unicode)
    last_seen = Column(Date)
    favorites = Column(Blob)
    cv = Column(Blob)

class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship('City', back_populates='children')
    employer_id = Column(Integer, ForeignKey('employer.id'))
    employer = relationship('Employer', back_populates='children')
    source_id = Column(Integer, ForeignKey('website.id'))
    website = relationship('Website', back_populates='children')
    language_id = Column(Integer, ForeignKey('language_id'))
    language = relationship('Language', back_populates='children')
    creation_date = Column(Date)
    update_date = Column(Date)
    title = Column(Integer)
    description = Column(Integer)
    salary = Column(Integer)
    sponsors_visa = Column(Boolean)
    url = Column(Unicode)
    skills = Column(PickleType)


Index('index', Job.title, unique=True, mysql_length=255)

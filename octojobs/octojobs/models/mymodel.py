from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
)

from .meta import Base


class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    city = Column(Unicode)
    employer = Column(Unicode)
    source_url = Column(Unicode)
    language = Column(Unicode)
    tile = Column(Integer)
    description = Column(Integer)


# Index('index', Job.title, unique=True, mysql_length=255)

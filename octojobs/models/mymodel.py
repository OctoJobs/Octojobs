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
    company = Column(Unicode)
    url = Column(Unicode)
    language = Column(Unicode)
    title = Column(Unicode)
    description = Column(Unicode)


# Index('index', Job.title, unique=True, mysql_length=255)

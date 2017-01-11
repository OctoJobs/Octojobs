# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from octopus.settings import DATABASE
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from octojobs.models.meta import Base
from octojobs.models.mymodel import Job


def db_connect():
    """Connect to database; return sqlalchemy engine instance."""
    return create_engine(URL(**DATABASE))


def create_job_table(engine):
    """Create a table."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class OctopusPipeline(object):
    """Create a pipeline that takes item instances from the scrape.
    The pipeline then adds those item instances to our database tables.
    """

    def __init__(self):
        """Initialize the database engine and sessionmaker.

        Sets up engine using our db_connect function, which creates an engine.
        Creates a table for our job instances by passing that engine into
        create_job_table(engine). Then, initializes the session.
        """
        engine = db_connect()
        create_job_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save item instances into the database."""
        session = self.Session()
        for key in item:
            job = Job(**item[key])

            try:
                session.add(job)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

        return item

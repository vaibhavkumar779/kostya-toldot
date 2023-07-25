import os

from sqlalchemy import Column, Integer, String, Date, create_engine, ForeignKey
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

from scraper import settings

DeclarativeBase = declarative_base()


def db_connect() -> Engine:
    """
    Creates database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    # return create_engine(URL(**settings.DATABASE))
    db_url = os.environ['DATABASE_URL']
    db_url = db_url.replace('postgres://', 'postgresql://')
    return create_engine(db_url)

def create_items_table(engine: Engine):
    """
    Create the Items table
    """
    DeclarativeBase.metadata.create_all(engine)


class AuthorDB(DeclarativeBase):
    __tablename__ = "AUTHORS"

    id = Column('id', String, primary_key=True)
    name = Column("name", String)
    url = Column("url", String)
    pic_url = Column("pic_url", String, nullable=True)


class PodcastDB(DeclarativeBase):
    __tablename__ = "PODCASTS"

    id = Column('id', String, primary_key=True)
    name = Column('name', String)
    description = Column('description', String, nullable=True)
    url = Column('url', String)

    # last_episode_id = Column('last_episode_id', ForeignKey('EpisodeModel.id'), nullable=True)
    last_episode_id = Column('last_episode_id', nullable=True)

    episode_amount = Column('episode_amount', Integer)
    tags = Column('tags', String, nullable=True)
    rss_url = Column('rss_url', String, nullable=True)


class EpisodeDB(DeclarativeBase):
    __tablename__ = "EPISODES"

    id = Column('id', String, primary_key=True)
    name = Column('name', String)
    description = Column('description', String, nullable=True)
    url = Column('url', String)

    audio_url = Column('audio_url', String)
    tags = Column('tags', String, nullable=True)

    pub_date = Column('pub_date', Date, nullable=True)
    length = Column('length', Integer, nullable=True)

    # podcast_id = Column('podcast_id', ForeignKey('PodcastModel.id'), nullable=True)
    # author_id = Column('author_id', ForeignKey('AuthorModel.id'), nullable=True)
    podcast_id = Column('podcast_id', nullable=True)
    author_id = Column('author_id', nullable=True)

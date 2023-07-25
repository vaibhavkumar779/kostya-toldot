# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy.orm import sessionmaker

from scraper.items import EpisodeItem, AuthorItem, PodcastItem
from scraper.models import AuthorDB, PodcastDB, EpisodeDB, db_connect

from utils import string2date


class ScraperPipeline:
    def __init__(self):
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if type(item) is AuthorItem:
            self.save_author_item(item)

        elif type(item) is PodcastItem:
            self.save_podcast_item(item)

        elif type(item) is EpisodeItem:
            self.save_episode_item(item)

        return item

    def save_author_item(self, author_item: AuthorItem):
        session = self.Session()
        query = session.query(AuthorDB).filter_by(id=author_item['id'])
        author_db = query.one_or_none()

        if author_db:
            query.update(dict(author_item))
            session.commit()
            session.close()
            return
        author_db = AuthorDB(**author_item)

        with session:
            session.add(author_db)
            session.commit()

    def save_podcast_item(self, podcast_item: PodcastItem):
        if podcast_item['tags']:
            podcast_item['tags'] = ';'.join(podcast_item['tags'])

        session = self.Session()
        query = session.query(PodcastDB).filter_by(id=podcast_item['id'])
        podcast_db = query.one_or_none()

        if podcast_db:
            query.update(dict(podcast_item))
            session.commit()
            session.close()
            return

        podcast_db = PodcastDB(**podcast_item)

        with session:
            session.add(podcast_db)
            session.commit()

    def save_episode_item(self, episode_item: EpisodeItem) -> EpisodeItem:
        if episode_item.get('last_episode_in_podcast') is not None:
            last_episode_in_podcast = episode_item.pop('last_episode_in_podcast')
        else:
            last_episode_in_podcast = False

        if episode_item['tags']:
            episode_item['tags'] = ';'.join(episode_item['tags'])
        if episode_item['pub_date']:
            episode_item['pub_date'] = string2date(episode_item['pub_date'])

        session = self.Session()
        query = session.query(EpisodeDB).filter_by(id=episode_item['id'])
        episode_db = query.one_or_none()

        if episode_db:
            query.update(dict(episode_item))
            session.commit()
            session.close()
            return

        episode_db = EpisodeDB(**episode_item)

        with session:
            session.add(episode_db)
            if last_episode_in_podcast:
                podcast_id = episode_item['podcast_id']
                session.query(PodcastDB).filter_by(id=podcast_id).update({'last_episode_id': episode_item['id']})
            session.commit()

        return episode_item

    def close_spider(self, spider):
        self.Session.close_all()

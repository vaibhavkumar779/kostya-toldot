# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class AuthorItem(Item):
    id = Field()
    name = Field()
    url = Field()
    pic_url = Field()


class PodcastItem(Item):
    id = Field()
    name = Field()
    description = Field()
    url = Field()
    last_episode_id = Field()
    episode_amount = Field()
    tags = Field()
    rss_url = Field()


class EpisodeItem(Item):
    id = Field()
    name = Field()
    description = Field()
    url = Field()
    audio_url = Field()
    tags = Field()

    pub_date = Field()
    length = Field()

    podcast_id = Field()
    author_id = Field()

    last_episode_in_podcast = Field()


if __name__ == '__main__':
    episode = EpisodeItem(name='gsdfsdfsd')
    episode['id'] = '2332'
    print(episode, type(episode))
    episode = dict(episode)
    print(episode, type(episode))
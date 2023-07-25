from scrapy import Spider, Request
from scrapy.http import Response

from scraper.items import EpisodeItem, AuthorItem, PodcastItem

author = AuthorItem(
    id='Noson Arister',
    name='Носон Аристер',
    url='http://aristermp3.com/wp/',
    pic_url='http://aristermp3.com/wp/wp-content/uploads/2014/12/Shiur_PB_300.jpg'
)

podcast = PodcastItem(
    id='arister_website',
    name='R. Natan Arister - ALL',
    description='Подкасты от Носон Аристер',
    url='http://aristermp3.com/wp/',
    tags=['Носон Аристер', 'Noson Arister'],
    rss_url='http://aristermp3.com/wp/feed/'
)


class AristerSpider(Spider):
    name = 'arister'
    allowed_domains = ['aristermp3.com']
    base_url = 'https://aristermp3.com'
    start_page = 'http://aristermp3.com/wp/'

    episodes_amount = 0

    def start_requests(self):
        yield Request(self.start_page, callback=self.parse_start_page)

    def parse_start_page(self, response: Response, **kwargs):
        first_post = response.css('div#boxes article')
        first_post_link = first_post.css('h2 a').attrib['href']
        yield author
        yield Request(first_post_link, callback=self.parse_episode_page, cb_kwargs=dict(last_episode=True))

    def parse_episode_page(self, response: Response, last_episode=False, **kwargs):
        main_content = response.css('div#primary')

        episode_id = main_content.css('article').attrib.get('id')
        db_id = "arister_" + episode_id
        if last_episode:
            podcast['last_episode_id'] = db_id
        name = main_content.css('h1.entry-title ::text').get()
        pub_date = main_content.css('time')
        if pub_date.get() is not None:
            pub_date = pub_date.attrib['datetime'].split('(')[1][:-1:]
        else:
            pub_date = None
        tags = main_content.css('footer p.tags a ::text').getall()
        url = response.url
        audio_url = main_content.css('div.entry-content a')
        if audio_url.get() is not None:
            audio_url = audio_url.attrib['href']
        else:
            audio_url = None

        description = response.css(f'#{episode_id} div p em').xpath('text()').get()
        if description:
            description = description.strip()

        if None not in [name, audio_url, url]:
            self.episodes_amount += 1
            episode_dict = dict(id=db_id, name=name, pub_date=pub_date, tags=tags, url=url, audio_url=audio_url,
                                description=description, podcast_id=podcast['id'], author_id=author['id'])
            yield EpisodeItem(**episode_dict)

        nav = main_content.css('div#posts-pagination')
        prev = nav.css('div.previous a')
        if prev.get() is not None:
            next_link = prev.attrib['href']
        else:
            next_link = None

        if next_link is not None:
            yield Request(next_link, callback=self.parse_episode_page)
        else:
            podcast['episode_amount'] = self.episodes_amount
            yield podcast

    def close(self, reason):
        pass

from datetime import date, timedelta

from scrapy import Spider, Request
from scrapy.http import Response
from scrapy.selector import Selector

from scraper.items import EpisodeItem, AuthorItem, PodcastItem
from utils import string2date

RSS_URL = f'https://toldot.com/rss/iTunesPodcasts/podcast_%s.rss'


class ToldotSpider(Spider):
    name = 'toldot'
    allowed_domains = ['toldot.com']
    base_url = 'https://toldot.com'
    cycles_url = f'{base_url}/cycles/'
    audios_url = f'{cycles_url}?razdel=1332'

    # start_urls = []
    def __init__(self, last_parsed=None, **kwargs):
        if last_parsed:
            self.last_parsed = date.fromisoformat(last_parsed)
        else:
            self.last_parsed = None
        super().__init__(**kwargs)

    def start_requests(self):
        yield Request(self.audios_url, callback=self.parse_pages)

    def parse_pages(self, response: Response, **kwargs):
        pages_selector = 'div.cycles_list > div.catalog-pagination:first-of-type li a'
        pages = response.css(pages_selector)
        pages_amount = len(pages)
        for i, page in enumerate(pages):
            # priority = pages_amount - i
            priority = 0
            page: Selector
            page_url = page.attrib['href']

            yield Request(f'{self.cycles_url}{page_url}', callback=self.parse_podcasts, priority=priority,
                          cb_kwargs={'priority': priority}, dont_filter=True)

    def parse_podcasts(self, response: Response, priority=0, **kwargs):
        podcasts_selector = 'div.cycles_list > table.links-table tr td a.icon.cycle'
        dates_selector = "div.cycles_list > table.links-table tr td.details ::text"

        podcasts = response.css(podcasts_selector)
        dates = response.css(dates_selector).getall()

        for _date, podcast_object in zip(dates, podcasts):
            date_string = _date.strip()
            dt = string2date(date_string)
            if self.last_parsed is not None and self.last_parsed - timedelta(days=2) > dt:
                continue
            podcast_url = podcast_object.attrib['href']
            yield Request(f'{self.base_url}{podcast_url}', callback=self.parse_episodes, priority=priority)

    def parse_episodes(self, response: Response, priority=0, **kwargs):
        main_content: Selector = response.css('div[itemprop="mainContentOfPage"]')

        podcast_url = response.url
        podcast_name = main_content.css('h1 ::text').get()
        podcast_id = podcast_url.split('cycles_')[1][:-5:]
        podcast_id_db = f'toldot_podcast_{podcast_id}'
        podcast_rss_url = RSS_URL % podcast_id

        description = main_content.css('div.cycle-info-container div.description ::text').get()
        if description:
            description = description.strip()

        episodes = main_content.css('ol li.cicles a')
        episode_amount = len(episodes)
        last_episode_url = episodes[-1].attrib['href']
        last_episode_id = last_episode_url.split('/')[-1][:-5:].strip()

        details: Selector = main_content.css('div.cycle-info-container p.details')

        tags = details.css('a.tegs ::text').getall()

        # YIELDING PODCAST INFO
        podcast_dict = dict(id=podcast_id_db, name=podcast_name, url=podcast_url, tags=tags,
                            description=description, episode_amount=episode_amount, rss_url=podcast_rss_url,
                            last_episode_id=last_episode_id)
        podcast_item = PodcastItem(**podcast_dict)
        yield podcast_item

        for i, episode in enumerate(episodes):
            episode_url = self.base_url + episode.attrib['href']
            yield Request(episode_url, callback=self.parse_episode, priority=priority,
                          cb_kwargs=dict(
                              podcast_id=podcast_id_db
                          ))

    def parse_episode(self, response: Response, podcast_id=None, **kwargs):
        main_content: Selector = response.css('div[itemprop="mainContentOfPage"]')

        details: Selector = main_content.css('div.audio-info-container p.details')

        author = details.css('a')
        author_name = author.css('::text').get().strip()
        author_url = self.base_url + author.attrib['href']
        author_link_id = author_url.split('author=')[1].strip()
        author_id = f'toldot_author_{author_link_id}'
        author_pic = main_content.css('div.author-photo')
        author_pic_url = author_pic.attrib.get('style')

        if author_pic_url:
            author_pic_url = self.base_url + author_pic_url.split('url(')[1][1:-3:]

        # YIELDING AUTHOR INFO
        author_dict = dict(id=author_id, name=author_name, url=author_url, pic_url=author_pic_url)
        author_item = AuthorItem(**author_dict)
        yield author_item

        episode_url = response.url
        episode_name = main_content.css('h1 ::text').get().strip()
        episode_id = episode_url.split('/')[-1][:-5:].strip()
        episode_id_db = f'toldot_episode_{episode_id}'

        tags = details.css('a.tegs ::text').getall()
        description = main_content.css('div.audio-info-container p.description ::text').get()
        if description:
            description = description.strip()
        pub_date = main_content.css('span.pubdate').attrib['title']

        download = main_content.css('div.audio-bar ul.download')
        duration = download.css('li ::text').get()
        download_link = download.css('li a.tegs[download="download"]').attrib['href']
        duration = list(map(int, duration.strip().split(':')))
        if len(duration) == 3:
            duration_hours, duration_min, duration_sec = duration
        elif len(duration) == 2:
            duration_min, duration_sec = duration
            duration_hours = 0
        else:
            duration_sec = duration
            duration_min = duration_hours = 0

        duration_in_seconds = duration_hours * 60 * 60 + duration_min * 60 + duration_sec

        # YIELDING EPISODE INFO
        episode_dict = dict(id=episode_id_db, name=episode_name, url=episode_url,
                            description=description, tags=tags, pub_date=pub_date, podcast_id=podcast_id,
                            author_id=author_id,
                            length=duration_in_seconds, audio_url=download_link)
        episode_item = EpisodeItem(**episode_dict)
        yield episode_item

    def close(self, spider):
        pass

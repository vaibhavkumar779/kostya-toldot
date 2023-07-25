import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from sqlalchemy.orm import sessionmaker
from scraper.models import db_connect, EpisodeDB, PodcastDB, AuthorDB

engine = db_connect()
Session = sessionmaker(bind=engine)
with Session() as session:
    posts = session.query(EpisodeDB).filter(EpisodeDB.id.startswith('arister')).all()

chrome = Chrome()
for post in posts:
    url = post.url
    print(url, post.id)
    chrome.get(url)
    time.sleep(0.5)

    try:
        audio = chrome.find_element(By.CSS_SELECTOR, 'audio')
    except NoSuchElementException as e:
        print('[ERROR]', e)
        continue
    except Exception as e:
        print('[ERROR]', e)
        continue
    play_btn = chrome.find_element(By.CSS_SELECTOR, 'span.map_play')
    play_btn.click()

    duration = 'NaN'
    while duration == 'NaN':
        try:
            duration = audio.get_attribute('duration')
        except:
            pass
        play_btn.click()
        time.sleep(0.5)

    duration = int(float(duration))
    print(duration)
    with Session() as session:
        session.query(EpisodeDB).filter_by(id=post.id).update({'length': duration})
        session.commit()


chrome.close()

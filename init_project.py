from datetime import date
import json
import os

from scraper.models import db_connect, EpisodeDB, AuthorDB, PodcastDB
from sqlalchemy.orm import sessionmaker
import django


author = AuthorDB(
    id='Noson Arister',
    name='Носон Аристер',
    url='http://aristermp3.com/wp/',
    pic_url='http://aristermp3.com/wp/wp-content/uploads/2014/12/Shiur_PB_300.jpg'
)

podcast = PodcastDB(
    id='arister_website',
    name='R. Natan Arister - ALL',
    description='Подкасты от Носон Аристер',
    url='http://aristermp3.com/wp/',
    tags='Носон Аристер;Noson Arister',
    rss_url='http://aristermp3.com/wp/feed/',
    episode_amount=165,
    last_episode_id='arister_post-558'
)


def add_to_db(db_obj, db_type, _session_maker):
    db_obj_dict: dict = db_obj.__dict__
    db_obj_dict.pop('_sa_instance_state')

    session = _session_maker()
    query = session.query(db_type).filter_by(id=db_obj.id)
    got_db_obj = query.one_or_none()

    if got_db_obj:
        print(f'Updated object with id: {db_obj_dict.get("id")}')
        query.update(dict(db_obj_dict))
        session.commit()
        session.close()
        return
    new_db_obj = db_type(**db_obj_dict)

    with session:
        print(f'Added object with id: {db_obj_dict.get("id")}')
        session.add(new_db_obj)
        session.commit()


def django_make_migrations():
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')


def populate_db():
    engine = db_connect()
    Session = sessionmaker(bind=engine)

    with open('arister_db_data.json') as file:
        data = json.load(file)

    posts_data_db = []
    for post in data:
        post['pub_date'] = date.fromisoformat(post['pub_date'])
        episode = EpisodeDB(**post)
        posts_data_db.append(episode)

    add_to_db(author, AuthorDB, Session)
    add_to_db(podcast, PodcastDB, Session)
    for post in posts_data_db:
        add_to_db(post, EpisodeDB, Session)


def create_super_user(username, password, email="", first_name="", last_name=""):
    django.setup()
    from django.contrib.auth.models import User
    invalid_inputs = ["", None]

    if username.strip() in invalid_inputs or password.strip() in invalid_inputs:
        return None

    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()

    return user


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    django_make_migrations()
    populate_db()
    create_super_user('root', '654zz321xx')

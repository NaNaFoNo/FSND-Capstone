import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
import json

# database_path ='postgresql://postgres:postgres@localhost:5432/capstone'
database_path = os.environ['DATABASE_URL']

if database_path[:10] != 'postgresql':
    database_path = database_path.replace('postgres', 'postgresql')

db = SQLAlchemy()

'''
setup_db(app)
    setup flask application with SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def test_setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Table: Podcasts
List of all Podcasts
'''


class Podcast(db.Model):
    __tablename__ = 'podcasts'

    id = Column(Integer, primary_key=True)
    author = Column(String)
    name = Column(String)
    image_link = Column(String(500))
    podcast_link = Column(String(120))
    speakers = relationship(
                    'Speaker',
                    secondary='episodes',
                    backref='podcasts',
                    viewonly=True
                )
    episodes = relationship('Episode', viewonly=True)

    def __init__(self, author, name, image, podcast_link):
        self.author = author
        self.name = name
        self.image_link = image
        self.podcast_link = podcast_link

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'author': self.author,
            'name': self.name,
            'image': self.image_link,
            'podcast_link': self.podcast_link,
            'speakers': len(self.speakers),
            'episodes': len(self.episodes)
        }


'''
Table: Speakers
List of Guest Speakers
'''


class Speaker(db.Model):
    __tablename__ = 'speakers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    image_link = Column(String(500))
    twitter_link = Column(String(120))
    website_link = Column(String(120))
    episodes = relationship('Episode', viewonly=True)

    def __init__(self, name, image_link, twitter_link, website_link):
        self.name = name
        self.image_link = image_link
        self.twitter_link = twitter_link
        self.website_link = website_link

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_link': self.image_link,
            'twitter_link': self.twitter_link,
            'website_link': self.website_link,
            'episodes': len(self.episodes)
        }


'''
Table: Episodes
List if Episodes
'''


class Episode(db.Model):
    __tablename__ = 'episodes'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    topics = Column(String)
    podcast_link = Column(String)
    speaker_id = Column(Integer, ForeignKey('speakers.id'), nullable=False)
    speaker_name = relationship('Speaker', viewonly=True)
    podcast_id = Column(Integer, ForeignKey('podcasts.id'), nullable=False)
    podcast_name = relationship('Podcast', viewonly=True)
    # start_time = Column(DateTime())
    # finished = Column(Boolean, default=False, nullable=False)

    def __init__(self, title, topics, podcast_link, podcast_id, speaker_id):
        self.title = title
        self.topics = topics
        self.podcast_link = podcast_link
        self.speaker_id = speaker_id
        self.podcast_id = podcast_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'topics': self.topics,
            'podcast_link': self.podcast_link,
            'speaker_id': self.speaker_id,
            'speaker_name': self.speaker_name.name,
            'podcast_id': self.podcast_id,
            'podcast_name': self.podcast_name.name,
            # 'published': self.start_time,
            # 'finished': self.finished
        }

import os
from sqlite3 import IntegrityError
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Posts
Have subject, content, and poster
'''
class Post(db.Model):  
  __tablename__ = 'posts'

  id = Column(Integer, primary_key=True)
  subject = Column(String)
  content = Column(String)

  def __init__(self, subject='', content=''):
    self.subject = subject
    self.content = content

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
      'subject': self.subject,
      'content': self.content
    }

'''
Replies
Have id of the post replied and content
'''
class Reply(db.Model):  
  __tablename__ = 'replies'

  id = Column(Integer, primary_key=True)
  post_id = Column(Integer)
  content = Column(String)

  def __init__(self, post_id, content=''):
    self.post_id = post_id
    self.content = content

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'post_id': self.post_id,
      'content': self.content
    }
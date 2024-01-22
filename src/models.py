import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    # Define relationships for followers and following
    followers = relationship('Follow', foreign_keys='Follow.user_to_id', back_populates='following_user')
    following = relationship('Follow', foreign_keys='Follow.user_from_id', back_populates='follower_user')

class Follow(Base):
    __tablename__ = 'follow'
    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    # Define relationships for the user who is being followed and the follower
    following_user = relationship('User', foreign_keys=[user_to_id], back_populates='followers')
    follower_user = relationship('User', foreign_keys=[user_from_id], back_populates='following')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    
    # Define relationship with User
    user = relationship('User', back_populates='posts')

    # Define relationship with Media
    media = relationship('Media', back_populates='post')

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', name='media_type_enum'), nullable=False)
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'))
    # Define relationship with Post
    post = relationship('Post', back_populates='media')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    # Define relationships with User and Post
    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')
    
## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
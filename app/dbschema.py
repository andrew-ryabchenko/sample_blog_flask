"""This module declares the database metadata and emits corresponding CREATE statements."""

#pylint: disable=import-error disable=too-few-public-methods
from os import getenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase
from flask_login import UserMixin

DB_PATH = getenv('DB_PATH', 'prod.db')
ENGINE = create_engine(f'sqlite:///{DB_PATH}', echo=True)

#Declarative base
class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM."""

# Defining the user table. This is the table that will store the user credentials used for
# authentication. The table will have three columns: id, email, and password_hash.
class User(Base, UserMixin):
    """User table."""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    username = Column(String)
    password_hash = Column(String)
    admin = Column(Boolean, default=False)

# Defining the post table. This is the table that will store the blog posts.
class Post(Base):
    """Post table."""
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    #Title of the post
    title = Column(String(length=50))
    #Short Description fo the post
    excerpt = Column(String(length=200))
    #Main content body of the post
    content = Column(String)
    #Capitalized tag
    tag = Column(String(length=50))
    #Post timestamp
    timestamp = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

# Emitting the schema to the database
Base.metadata.create_all(ENGINE)

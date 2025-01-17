"""This module defines the database models for the application."""

#pylint: disable=import-error
from datetime import datetime as dt
from flask import g
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.dbschema import User, Post, ENGINE
from app.util import password_hash

def get_session():
    """Returns a session object."""
    if not hasattr(g, "db_session"):
        setattr(g, "db_session", Session(ENGINE))
        return g.db_session
    return g.db_session

def validate_user(email: str, password: str) -> User | None:
    """Validates user credentials.
    Returns User instance if user exists, otherwise returns None."""
    #Get session object
    session = get_session()
    #Generate password hash
    pswd_hash = password_hash(password)
    #Instantiate User object
    user = User(email=email, password_hash=pswd_hash)
    #Get this user from database
    user = session.execute(select(User).where(User.email == user.email).
                           where(User.password_hash == pswd_hash)).scalar_one_or_none()
    #Return user if user exists, otherwise return None
    return user if user else None

def load_user(user_id: str) -> User | None:
    """Loads user from database by id."""
    #Get session object
    session = get_session()
    #Get user from database
    user = session.get(User, int(user_id))
    #Return user
    return user

def add_user(email:str, username: str, password:str, admin=False) -> User:
    """Adds user to database."""
    #Get session object
    session = get_session()
    #Generate password hash
    pswd_hash = password_hash(password)
    #Instantiate User object
    user = User(email=email.lower(),
                username = username.lower(),
                password_hash=pswd_hash, admin=admin)
    #Add user to session
    session.add(user)
    session.flush()
    session.commit()
    # Return User instance of newly inserted user
    return user

def check_email_exists(email: str) -> bool:
    """Checks if user with given email already exists in the database."""
    #Get session object
    session = get_session()
    #Get user from database
    user = session.execute(select(User).where(User.email == email)).scalar_one_or_none()
    #Return True if user exists, otherwise return False
    return bool(user)

def check_username_exists(username: str) -> bool:
    """Checks if user with given username already exists in the database."""
    #Get session object
    session = get_session()
    #Get user from database
    user = session.execute(select(User).where(User.username == username)).scalar_one_or_none()
    #Return True if user exists, otherwise return False
    return bool(user)

def add_post(title: str, excerpt: str, content: str, tag: str, user_id: int) -> int:
    """Adds post to database."""
    #Capitalize tag
    tag = tag.capitalize()
    #Get current unix timestamp
    timestamp = dt.now().strftime("%m/%d/%Y, %H:%M")
    #Get session object
    session = get_session()
    #Instantiate Post object
    post = Post(title=title, excerpt=excerpt,
                content=content, tag=tag,
                timestamp=timestamp, user_id=user_id)
    #Add post to session
    session.add(post)
    session.flush()
    post_id = post.id
    session.commit()
    # Return post_id of newly inserted post
    return post_id

def get_posts(limit=100, offset=0) -> list[Post]:
    """Fetches at most 100 posts from the database."""
    #Get session object
    session = get_session()
    posts = session.execute(select(Post, User.username).
                    limit(limit).
                    offset(offset).
                    join_from(Post, User, Post.user_id == User.id).
                    order_by(Post.timestamp.desc()))
    posts = posts.all()
    return posts

def get_post(post_id: str) -> Post:
    """Fetches single post form the database identified by post_id"""
    #Get session object
    session = get_session()
    post = session.execute(select(Post, User.username).
                    where(Post.id == post_id).
                    join_from(Post, User, Post.user_id == User.id))
    #Fetch post and return Post object
    post = post.first()

    return post

def get_users() -> list[User]:
    """Fetches all users from the database."""
    #Get session object
    session = get_session()
    #Pylint complains about using == with None, but this is the correct way to do it
    #pylint: disable=singleton-comparison
    users = session.execute(select(User).where(User.admin == False))
    #Fetch users and return list of User objects
    users = users.all()

    return users

def filter_posts(tag: str = None, username: str = None, title: str = None,
                 limit: int = 100, offset: int = 0) -> list[Post]:
    """Filters posts by tag, username, and title."""
    #Get session object
    session = get_session()
    #Get posts from database
    #Build select query
    stmt = select(Post, User.username)
    #Add additional state onto query object if tag, username, or title is not None
    if tag:
        stmt = stmt.where(Post.tag.like(f"%{tag}%"))
    if username:
        stmt = stmt.where(User.username.like(f"%{username}%"))
    if title:
        stmt = stmt.where(Post.title.like(f"%{title}%"))

    #Add additional constraints to query object
    stmt = stmt.join_from(Post, User, Post.user_id == User.id) \
                                .limit(limit).offset(offset) \
                                .order_by(Post.timestamp.desc())
    #Execute query
    posts = session.execute(stmt)
    #Fetch posts and return list of Post objects
    posts = posts.all()

    return posts

def get_user_posts(user_id: int, limit: int = 100, offset: int = 0) -> list[Post]:
    """Fetches posts from the database created by user_id."""
    #Get session object
    session = get_session()
    #Get posts from database
    posts = session.execute(select(Post, User.username).
                    where(Post.user_id == user_id).
                    join_from(Post, User, Post.user_id == User.id).
                    limit(limit).
                    offset(offset).
                    order_by(Post.timestamp.desc()))
    #Fetch posts and return list of Post objects
    posts = posts.all()

    return posts

def delete_post(post_id: int, user_id: id) -> None:
    """Deletes post from database."""
    #Get session object
    session = get_session()
    #Only deletes post if logged in user owns the post
    session.execute(delete(Post).where(Post.id == post_id).where(Post.user_id == user_id))
    session.commit()

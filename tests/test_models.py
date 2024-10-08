"""This module defines tests for database models located in app.models module."""
#pylint: disable=import-error disable=unused-argument
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import get_session, validate_user, load_user, add_user, get_user_posts
from app.models import check_email_exists, check_username_exists, add_post
from app.models import get_post, get_posts, get_users, filter_posts, delete_post
from app.dbschema import User, Post

def test_get_session(g, mocker):
    """Confirms that get_session function properly
    handles storage and retrieval of db_session
    from g context object."""
    #Set mocked db_session on simulated g object
    setattr(g, "db_session", 13)
    #Patch autheentic g object
    mocker.patch("app.models.g", g)
    #Get session object
    session = get_session()

    #Assert if session object is equal to mocked db_session
    assert session == 13

    #Remove mocked db_session from g object
    delattr(g, "db_session")
    #Get session object
    session = get_session()

    #Assert if session object is a real newly ccreated session object
    assert isinstance(session, Session)

def test_validate_user(mocker, test_user, session):
    """Confirms that validate_user function properly
    validates user credentials."""
    #Mock get_session function
    mocker.patch("app.models.get_session", return_value=session)
    #Mock return value of password_hash function
    mocker.patch("app.models.password_hash", return_value="password")
    #Create mocked User object
    user = validate_user("andrew@gmail.com", "password")

    #Assert if user is not None
    assert user is not None
    assert isinstance(user, User)

def test_load_user(test_user, mocker, session):
    """Confirms that load_user function properly
    loads test user from database by id."""
    #Mock get_session function
    mocker.patch("app.models.get_session", return_value=session)
    #Load test user
    user = load_user(test_user.id)
    #Assert if user is not None
    assert user is not None
    assert isinstance(user, User)

    #Load non-existing user
    user = load_user(2)
    #Assert if user is None
    assert user is None

def test_add_user(mocker, session):
    """Confirms that add_user function properly
    adds user to database."""
    #Mock get_session function
    mocker.patch("app.models.get_session", return_value=session)
    #Mock return value of password_hash function
    mocker.patch("app.models.password_hash", return_value="password")
    #Add user to database
    add_user("mike@gmail.com", "mike", "password")

    #Get user from database
    user = session.execute(select(User).where(User.email == "mike@gmail.com")).scalar_one_or_none()
    #Assert if user is not None
    assert user is not None

def test_check_email_exists(mocker, test_user, session):
    """Confirms that check_email_exists function properly
    checks if user with given email already exists in the database."""
    #Mock get_session function
    mocker.patch("app.models.get_session", return_value=session)
    #Check if test user exists
    assert check_email_exists(test_user.email)

    #Check if non-existing email exists
    assert not check_email_exists(test_user.email + "1")

def test_check_username_exists(mocker, test_user, session):
    """Confirms that check_username_exists function properly
    checks if user with given username already exists in the database."""
    #Mock get_session function
    mocker.patch("app.models.get_session", return_value=session)
    #Check if test user exists
    assert check_username_exists(test_user.username)

    #Check if non-existing username exists
    assert not check_username_exists(test_user.username + "1")

def test_add_post(mocker, test_user, post, session):
    """Confirms that add_post function properly
    adds post to database."""
    #Mock get_session function
    mocker.patch("app.models.get_session", return_value=session)
    #Add post to database
    post_id = add_post(post["title"], post["excerpt"], post["content"], post["tag"], test_user.id)

    #Get post from database
    post = session.execute(select(Post).where(Post.title == post["title"])).scalar_one_or_none()
    #Assert if post is not None
    assert post.id == post_id

def test_get_post(mocker, session):
    """Confirms that get_post function properly
    gets post from database."""
    #Mock get_session function
    mocker.patch("app.models.get_session", return_value=session)
    #Get random post from database
    existing_post = session.execute(select(Post)).scalar_one_or_none()
    #Get post from database using get_post
    post = get_post(existing_post.id)[0]
    #Assert if post is not None
    assert isinstance(post, Post)
    #Assert if post is equal to existing_post
    assert post.title == existing_post.title

def test_get_posts(mocker, session):
    """Confirms that get_posts function properly
    gets a 100 posts from database."""
    #Mock get_session function
    mocker.patch("app.models.get_session", return_value=session)
    #Get posts from database
    existing_posts = session.execute(select(Post).
                                     order_by(Post.timestamp.desc())).all()

    #Get posts from database using get_posts
    posts = get_posts()
    #Assert if the number of posts retrieved by both methods is equal
    assert len(existing_posts) == len(posts)
    #Assert if posts are retrieved in same order
    for ex_post, post in zip(existing_posts, posts):
        #Assert if post is equal to existing_post
        assert post[0].id == ex_post[0].id
        assert post[0].title == ex_post[0].title

def test_get_users(mocker, session):
    """Confirms that get_users function properly
    gets all users from database ignoring admin users."""
    #Mock get_session function
    mocker.patch("app.models.get_session", return_value=session)
    #Get existing users from database
    #Pylint complains about == False comparison
    #pylint: disable=singleton-comparison
    existing_users = session.execute(select(User).
                                     where(User.admin==False)).all()

    #Get users from database using get_users
    users = get_users()
    #Assert if the number of users retrieved by both methods is equal
    assert len(existing_users) == len(users)

def test_filter_posts(mock_posts, mocker, session):
    """Confirms that filter_posts function properly."""

    #Mock get_session function
    mocker.patch("app.models.get_session", return_value=session)
    #Unpack mock posts
    username_post_mapping, tag_post_mapping, title_post_mapping = mock_posts

    #Testing filtering by username
    for username, posts in username_post_mapping.items():
        #Get posts from database using filter_posts function
        filtered_posts = filter_posts(username=username)
        #Assert if the number of posts retrieved by both methods is equal
        assert len(filtered_posts) == len(posts)

    #Testing filtering by tag
    for tag, posts in tag_post_mapping.items():
        #Get posts from database using filter_posts function
        filtered_posts = filter_posts(tag=tag)
        #Assert if the number of posts retrieved by both methods is equal
        assert len(filtered_posts) == len(posts)

    #Testing filtering by title
    for title, posts in title_post_mapping.items():
        #Get posts from database using filter_posts function
        filtered_posts = filter_posts(title=title)
        #Assert if the number of posts retrieved by both methods is equal
        assert len(filtered_posts) == len(posts)

def test_get_user_posts(mocker, session):
    """Confirms that get_user_posts function properly."""

    #Mock get_session function
    mocker.patch("app.models.get_session", return_value=session)
    #Get posts by id
    user_posts = get_user_posts(1)
    #Assert if the number of posts retrieved by both methods is equal
    assert len(user_posts) == 5

def test_delete_post(mocker, session):
    """Confirms that delete_post function properly"""
    #Mock get_session function
    mocker.patch("app.models.get_session", return_value=session)

    #Delete post
    delete_post(1, 1)

    #Verify that post is deleted
    post = session.execute(select(Post).where(Post.id == 1)).scalar_one_or_none()

    assert post is None

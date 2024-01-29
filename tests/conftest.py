import pytest
from flask import Flask
from app.dbschema import User, Post, ENGINE
from app import make_app
from sqlalchemy.orm import Session
from faker import Faker
from app.util import password_hash
from sqlalchemy import delete
from tests.mock_posts import generate_posts
from app.forms import RegisterForm

@pytest.fixture(scope="session")
def g():
    """Returns a simulateed g object."""
    class G:
        pass
    return G()

@pytest.fixture(scope="module")
def session():
    """Yields a session object."""
    session = Session(ENGINE)

    yield session

    #Clean up database before the next module is executed
    session.execute(delete(User))
    session.execute(delete(Post))
    session.commit()
    session.close()

@pytest.fixture(scope="module")
def test_user(session):
    """Creates and returns a test user."""
    user = User(
        id=1,
        email="andrew@gmail.com",
        username="andrew",
        password_hash="password",
        admin=True)
    session.add(user)
    session.flush()
    session.commit()

    return user

@pytest.fixture
def new_user(session) -> User:
    """Adds a random user to the database"""
    fkr = Faker()
    profile = fkr.simple_profile()
    user = User(username=profile["username"],
                email=profile["mail"],
                password_hash=password_hash("password"))
    
    session.add(user)
    session.commit()

    return user

@pytest.fixture(scope="session")
def post():
    """Returns dictionary respresenting mock post."""
    fkr = Faker()
    return {
        "title": fkr.sentence(5),
        "excerpt": fkr.sentence(10),
        "tag": fkr.word(),
        "content": fkr.sentence(100)
    }

@pytest.fixture(scope="session")
def current_user():
    """Creates user instance for patching current_user"""
    user = User(id=1)
    return user

@pytest.fixture(scope="module")
def app() -> Flask:
    """Configure instance of the application for testing."""
    app = make_app(login_disabled=True)
    return app

@pytest.fixture
def post_object(current_user):
    """Returns ORM mapped object Post."""
    fkr = Faker()
    obj = Post(
        id=1,
        title=fkr.sentence(5),
        excerpt=fkr.sentence(10),
        content=fkr.sentence(100),
        tag=fkr.word(),
        timestamp=fkr.date(),
        user_id=current_user.id
        )
    return obj

#When mock_posts fixturee is requested, it will triggeer the chain of fixture requests
#that will clean up the database, generate mock users, and generate mock posts.
@pytest.fixture(scope="module")
def clean_up(session):
    """Clean up the database."""
    session.execute(delete(User))
    session.execute(delete(Post))
    session.commit()

@pytest.fixture(scope="module")
def mock_users(clean_up):
    """Generates mock users for testing purposes."""
    from tests.mock_users import generate_users
    generate_users(5)

@pytest.fixture(scope="module")
def mock_posts(mock_users):
    """Generates mock posts for testing purposes.
    Returns mapping of users and their posts."""
    user_post_mapping = generate_posts(ppu=5)
    return user_post_mapping

@pytest.fixture(scope="module")
def form(test_user):
    """Returns a Form prefilled with test user credentials."""
    form = RegisterForm()
    form.email.data = test_user.email
    form.username.data = test_user.username
    form.password.data = "password"
    form.confirm_password.data = "password"
    return form
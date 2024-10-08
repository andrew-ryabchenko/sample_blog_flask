"""This module contains tests that are executed with authentication disabled
as if the user is authenticated."""
#pylint: disable=import-error disable=unused-argument
from flask import Flask
from sqlalchemy.orm import Session
from app.dbschema import ENGINE

def get_test_session():
    """Yields a session object for testing."""
    session = Session(ENGINE)
    return session

def test_index(app: Flask):
    """Test homepage."""
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Offcanvas with post filtering options" in response.data

def test_about(app: Flask):
    """Test about page."""
    client = app.test_client()
    response = client.get("/about")
    assert response.status_code == 200
    assert b"Our blog application is" in response.data

def test_add_post_v(app: Flask, post, current_user, mocker, session):
    """Test /add-post route."""
    mocker.patch('app.app.current_user', current_user)
    #Mock get_session function return value
    mocker.patch("app.models.get_session", return_value=session)

    client = app.test_client()
    #Testing POST method
    response = client.post("/add-post", data=post)

    assert response.status_code == 302
    assert response.headers["LOCATION"] == "/"

    #Testing GET method
    response = client.get("/add-post")

    assert response.status_code == 200
    assert b"<!-- New Post Form -->" in response.data


def test_read_post(app: Flask, post_object, mocker, session):
    """Test /read_post route."""
    mocker.patch("app.app.get_post", return_value=[post_object])
    #Mock get_session function return value
    mocker.patch("app.models.get_session", return_value=session)

    client = app.test_client()
    response = client.get("/read_post?id=1")

    assert response.status_code == 200
    assert bytes(post_object.title, "utf-8") in response.data

    #URL parameter is missing
    response = client.get("/read_post")

    assert response.status_code == 302

def test_delete_post(app: Flask, mocker, current_user, session):
    """Test /delete_post route."""
    # Mock current_user
    mocker.patch('app.app.current_user', current_user)
    # Mock delete user function
    mocker.patch('app.app.delete_post', return_value=None)
    # Mock get_session function return value
    mocker.patch("app.models.get_session", return_value=session)

    client = app.test_client()

    response = client.get("/delete_post?id=1", headers={
        "Referer": "/"
    })

    assert response.status_code == 302
    assert response.headers["Location"] == "/"

def test_apply_filter(app: Flask, post_object, mocker, session):
    """Test /apply-filter route."""
    #Mock filter_posts function
    mocker.patch("app.app.filter_posts",
                 return_value=[(post_object, "andrew@gmail.com")])

    #Mock get_session function return value
    mocker.patch("app.models.get_session", return_value=session)

    client = app.test_client()
    response = client.get("/apply-filter?title=test&username=test&tag=test")

    assert response.status_code == 200
    assert bytes(post_object.title, "utf-8") in response.data

    #Simulate the scenario when form does not validate
    #by providing one of the filed values longer than allowed
    response = client.get(f"/apply-filter?title={'t' * 51}&username=test&tag=test")

    assert response.status_code == 200
    assert b"Offcanvas with post filtering options" in response.data

def test_my_posts(app: Flask, mocker, post_object, current_user, session):
    """Test /my-posts route."""
    # Mock delete user function
    mocker.patch("app.app.get_user_posts",
                 return_value=[(post_object, "andrew@gmail.com")])
    #Mock get_session function return value
    mocker.patch("app.models.get_session", return_value=session)
    # Mock current_user so the get_user_posts call can be made
    mocker.patch("app.app.current_user", current_user)

    client = app.test_client()
    response = client.get("/my-posts", headers={
        "Referer": "/"
    })

    assert response.status_code == 200
    assert bytes(post_object.title, "utf-8") in response.data

def test_login(app: Flask):
    """Tests /login route."""

    client = app.test_client()
    response = client.get("/login")

    assert response.status_code == 200
    assert b"Login Form" in response.data

def test_register_get(app: Flask):
    """Tests /register route."""

    client = app.test_client()
    response = client.get("/register")

    assert response.status_code == 200
    assert b"Registration Form" in response.data

def test_register_post(app: Flask, mocker, current_user, session):
    """Tests /register route."""
    # Mock return value of add_user function
    mocker.patch("app.authentication.add_user",
                 return_value=current_user)

    #Mock get_session function return value
    mocker.patch("app.models.get_session", return_value=session)

    client = app.test_client()
    #Submit mock registration form to the endpoint
    response = client.post("/register", data={
        "email": "email",
        "username": "username",
        "password": "password",
        "confirm_password": "password"
    })

    assert response.status_code == 302
    assert "/" == response.headers["Location"]

def test_logout(app: Flask):
    """Tests /logout route."""

    client = app.test_client()
    response = client.get("/logout")

    assert response.status_code == 302
    assert "/login" == response.headers["Location"]

def test_clean_up(session):
    """Request fixture to trigger database clean-up before the next module."""

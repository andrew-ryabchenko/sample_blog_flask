"""This module contains tests that are executed with authentication enabled
as if the user is not authenticated."""

import pytest
from flask import Flask
from app import make_app
from sqlalchemy import select
from app.dbschema import User

@pytest.fixture(scope="module")
def app() -> Flask:
    """Configure instance of the application for testing."""
    return make_app(login_disabled=False)


def test_login(app: Flask, test_user, session, mocker):
    """Tests if /login route renders login page
    if client is not authenticated."""
    #Mock return value of get_session function
    mocker.patch("app.models.get_session", return_value=session)
    #Mock return value of password_hash function because 
    #test user in the database has unhashed value of password
    mocker.patch("app.models.password_hash", return_value="password")
    client = app.test_client()

    response = client.post("/login", data={
        "email": test_user.email,
        "password": "password"
    })
    #Check if user is redirected to homepage
    assert response.status_code == 302
    assert "/" == response.headers["Location"]

def test_register_post(app: Flask, test_user, session, mocker):
    """Confirm that user is returned registration page with errors
    if form validation fails."""
    #Mock return value of get_session function
    mocker.patch("app.models.get_session", return_value=session)
    
    client = app.test_client()

    #Provide email that already in-use by test account
    response = client.post("/register", data={
        "email": test_user.email,
        "username": test_user.username,
        "password": "password",
        "confirm_password": "password"
    })

    assert response.status_code == 200
    assert b"already in-use" in response.data

def test_index(app: Flask):
    """Tests if / route redireccts to login page
    if client is not authenticated."""

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_about(app: Flask):
    """Tests if /about route redirects to login page
    if client is not authenticated."""

    client = app.test_client()
    response = client.get("/about")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_add_post(app: Flask):
    """Tests if /add-post route redirects to login page
    if client is not authenticated."""

    client = app.test_client()
    response = client.get("/add-post")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_read_post(app: Flask):
    """Tests if /read_post route redirects to login page
    if client is not authenticated."""

    client = app.test_client()
    response = client.get("/read_post")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_delete_post(app: Flask):
    """Tests if /delete_post route redirects to login page
    if client is not authenticated."""

    client = app.test_client()
    response = client.get("/delete_post")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_apply_filter(app: Flask):
    """Tests if /apply-filter route redirects to login page
    if client is not authenticated."""

    client = app.test_client()
    response = client.get("/apply-filter")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_my_posts(app: Flask):
    """Tests if /my_posts route redirects to login page
    if client is not authenticated."""

    client = app.test_client()
    response = client.get("/my-posts")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_load_usr(test_user, session, mocker):
    """Test load_usr function that handles user loading
    for flask_login extension."""
    from app.app import load_usr

    #Mock return value of get_session function
    mocker.patch("app.models.get_session", return_value=session)

    #Check if user is loaded correctly
    assert load_usr(str(test_user.id)).id == test_user.id


def test_clean_up(session):
    """Clean up database before the next module."""
    pass

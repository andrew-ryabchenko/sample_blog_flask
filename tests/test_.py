"""This module tests Flask application by using Flask test client."""

import sys
import os
from flask import render_template, session

#Add current CWD to path so app module can be imported when debugging this module
sys.path.append(os.getcwd())

from app import app

def test_index():
    """Test homepage."""
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert render_template("home.html") == response.text

def test_login_get():
    """Test login page."""
    with app.test_client() as client:
        response = client.get("/login")
        assert response.status_code == 200
        assert render_template("login.html") == response.text

def test_login_post():
    """Test login post."""
    with app.test_client() as client:
        response = client.post("/login", data={"email": "andrew@gmail.com"})

        assert response.status_code == 302
        assert "/" == response.headers["Location"]

def test_register_get():
    """Test register page."""
    with app.test_client() as client:
        response = client.get("/register")
        assert response.status_code == 200
        assert render_template("register.html") == response.text

def test_register_post():
    """Test register post."""
    with app.test_client() as client:
        response = client.post("/register", data={"email": "andrew@gmail.com"})

        assert response.status_code == 302
        assert "/" == response.headers["Location"]

def test_logout():
    """Test logout route."""
    with app.test_client() as client:
        response = client.get("/logout")

        assert response.status_code == 302
        assert "/login" == response.headers["Location"]
        assert session.get("email") is None

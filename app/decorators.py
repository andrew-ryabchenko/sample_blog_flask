"""This module cocntains custom view function decorators that
support various parts of the application."""

from functools import wraps
from app.models import get_users
from flask import render_template
from flask_login import current_user
from flask_login.utils import login_required as login_required_flask_login

def login_required(view_func):
    """Custom version of login_required that checks if user is admin
    and handles the request accordingly. If admin is logged in,
    the admin version of website is returned."""
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.admin:
            #Admin Logic
            if view_func.__name__ != "logout":
                #Does not apply to logout view function because A
                #admin must be able to logout.
                #Fetch all users form the database.
                users = get_users()
                return render_template("admin_page.html", users=users)
        
        #Wrap view function with login_required by flask_login
        return login_required_flask_login(view_func)(*args, **kwargs)
        
    return wrapper

"""This module defines blueprint for authentication routes."""

from flask import Blueprint, render_template, request, redirect
from app.forms import register_form, login_form
from app.models import add_user, validate_user
from flask_login import login_user, logout_user
from app.decorators import login_required, already_logged_in

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
@already_logged_in
def login():
    """Login Form."""
    form = login_form(request.form)

    if request.method == "POST" and form.validate():
        #Validation has passed. User must exist in the database.
        #Fetch user from database
        user = validate_user(form.email.data, form.password.data)
        #Log the user in with flask-login
        login_user(user)
        #Redirect to homepage
        return redirect("/")
        
    #Render login page
    return render_template("login.html", form=form)

@auth.post("/register")
@already_logged_in
def register_post():
    """Register Form."""
    form = register_form(request.form)
   
    if form.validate():
        #Upon form validation it is certain that the email is not in-use
        #and that the passwords match.

        #Add user to database and collect user_id
        user = add_user(form.email.data, form.username.data, form.password.data)
        #Log the user in with flask-login
        login_user(user)
        #Redirect to homepage
        return redirect("/")
        
    #Render register page
    return render_template("register.html", form=form)

@auth.get("/register")
@already_logged_in
def register_get():
    """Register Form."""
    form = register_form()
    return render_template("register.html", form=form)

@auth.get("/logout")
@login_required
def logout():
    """Logout route."""
    #Log the user out with flask-login
    logout_user()
    #Redirect to login page
    return redirect("/login")

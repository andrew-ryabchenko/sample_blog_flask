"""This module implements a simple Flask app with routes for a homepage, login, and register page.
Authentication is not implemented yet, but the routes are there to handle the requests."""

from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "Hello World"
app.config["application_name"] = "Sample Blog Application"

@app.route("/")
def index():
    """Return homepage."""
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login Form."""
    if request.method == "POST":
        #TODO - Check if username exists
        session["email"] = request.form["email"]
        return redirect("/")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register Form."""
    if request.method == "POST":
        #TODO - Check if username already exists
        #TODO - Add user to database
        session["email"] = request.form["email"]
        return redirect("/")
    return render_template("register.html")

@app.route("/logout")
def logout():
    """Logout route."""
    #Clear user session
    session.pop("email", None)
    return redirect("/login")

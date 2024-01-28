"""This module implements a simple Flask app with routes for a homepage, login, and register page.
Authentication is not implemented yet, but the routes are there to handle the requests."""

from flask import Flask, render_template, request, redirect, g
from app.forms import register_form, login_form, new_post_form, filter_posts_form
from app.models import add_user, validate_user, load_user, add_post, get_posts, get_post, filter_posts
from secrets import token_hex
from flask_login import LoginManager, login_user, logout_user, current_user
from app.decorators import login_required

app = Flask(__name__)
#Generate a random secret key
app.secret_key = token_hex(32)
#Add application name to the global scope of Jinja templates
app.config["application_name"] = "Sample Blog"

#Initialize flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#User retrieval function for flask-login
@login_manager.user_loader
def load_usr(user_id: str):
    """Load user by id."""
    print("Loading user")
    return load_user(user_id)

@app.route("/")
@login_required
def index():
    """Return homepage with preview of latest hundred posts."""
    form = filter_posts_form(request.form)
    posts = get_posts()
    return render_template("home.html", posts=posts, form=form)

@app.route("/add-post", methods=["GET", "POST"])
@login_required
def add_post_v():
    """Return new post page."""
    form = new_post_form(request.form)

    if request.method == "POST" and form.validate():
        #Create new post
        add_post(form.title.data, form.excerpt.data, 
                 form.content.data, form.tag.data, 
                 current_user.id)
        #Redirect to homepage
        return redirect("/")
    
    return render_template("new_post.html", form=form)

@app.get("/read_post")
@login_required
def read_post():
    if "id" in request.args:
        referrer = request.referrer
        post_id = request.args["id"]
        post = get_post(post_id)
        return render_template("post_view.html", referrer=referrer, post=post)
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login Form."""
    form = login_form(request.form)

    if request.method == "POST" and form.validate():
        #Validation has passed. User must exist in the database.
        #Collect user_id from database
        user = validate_user(form.email.data, form.password.data)
        #Log the user in with flask-login
        login_user(user)
        #Redirect to homepage
        return redirect("/")
        
    #Render login page
    return render_template("login.html", form=form)

@app.get("/apply-filter")
@login_required
def apply_filter():
    """Fetch posts from database based on filter criteria."""
    form = filter_posts_form(request.args)
    #Get posts from database
    if form.validate():
        print("Form validated")
        posts = filter_posts(form.tag.data, form.username.data, form.title.data)
        #Render homepage with filtered posts
        return render_template("home.html", posts=posts, form=form)
    print("Form did not validate")
    #Render homepage with no posts
    return render_template("home.html", form=form)

@app.post("/register")
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
   
@app.get("/register")
def register_get():
    """Register Form."""
    form = register_form()
    return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
    """Logout route."""
    #Log the user out with flask-login
    logout_user()
    #Redirect to login page
    return redirect("/login")

@app.teardown_appcontext
def close_db_session(exception=None):
    """Closes the database session after each request."""
    db_session = g.pop('db_session', None)
    if db_session is not None:
        db_session.close()

if __name__ == "__main__":
    app.run(debug=True)

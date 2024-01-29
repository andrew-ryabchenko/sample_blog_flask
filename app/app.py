"""This module implements a simple Flask app with routes for a homepage, login, and register page.
Authentication is not implemented yet, but the routes are there to handle the requests."""

#pylint: disable=import-error disable=unused-argument
from secrets import token_hex
from flask import Flask, render_template, request, redirect, g
from flask_login import LoginManager, current_user
from app.forms import new_post_form, filter_posts_form
from app.models import load_user, add_post, get_posts, get_post
from app.models import filter_posts, get_user_posts, delete_post
from app.authentication import auth
from app.decorators import login_required

app = Flask(__name__)
#Generate a random secret key
app.secret_key = token_hex(32)
#Add application name to the global scope of Jinja templates
app.config["application_name"] = "Sample Blog"

#Register blueprints
app.register_blueprint(auth)

#Initialize flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

#User retrieval function for flask-login
@login_manager.user_loader
def load_usr(user_id: str):
    """Load user by id."""
    return load_user(user_id)

@app.route("/")
@login_required
def index():
    """Return homepage with preview of latest hundred posts."""
    form = filter_posts_form(request.form)
    posts = get_posts()
    return render_template("home.html", posts=posts, form=form)

@app.route("/about")
@login_required
def about():
    """Return about page."""
    return render_template("about.html")

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
    """Retrieve post from database and render post view page."""

    if "id" in request.args:
        referrer = request.referrer
        post_id = request.args["id"]
        post = get_post(post_id)
        return render_template("post_view.html", referrer=referrer, post=post)
    return redirect("/")

@app.get("/delete_post")
@login_required
def delete_post_v():
    """Delete post."""
    if "id" in request.args:
        post_id = request.args["id"]
        user_id = current_user.id
        #Delete post
        delete_post(post_id, user_id)
    #Redirect to previous page
    return redirect(request.referrer)

@app.get("/apply-filter")
@login_required
def apply_filter():
    """Fetch posts from database based on filter criteria."""
    form = filter_posts_form(request.args)
    #Get posts from database
    if form.validate():
        posts = filter_posts(form.tag.data, form.username.data, form.title.data)
        #Render homepage with filtered posts
        return render_template("home.html", posts=posts, form=form)
    #Render homepage with no posts
    return render_template("home.html", form=form)

@app.get("/my-posts")
@login_required
def my_posts():
    """Return posts created by current user."""
    referrer = request.referrer
    #Get posts from database
    posts = get_user_posts(user_id=current_user.id)
    #Render homepage with filtered posts
    return render_template("my_posts.html", posts=posts, referrer=referrer)

@app.teardown_appcontext
def close_db_session(exception=None):
    """Closes the database session after each request."""
    db_session = g.pop('db_session', None)
    if db_session is not None:
        db_session.close()

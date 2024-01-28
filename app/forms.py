from wtforms import Form, StringField, EmailField, PasswordField, TextAreaField
from wtforms import validators, ValidationError
from app.models import check_email_exists, validate_user, check_username_exists

def verify_email_in_use(form, email):
        """Custom field validator that checks if email is already in-use."""
        if check_email_exists(email.data):
            #User already exists, raise a validation error
            raise ValidationError(f"Email {email.data} already in-use.")

def check_credentials(form, email):
        """Custom field validator that check if email and password are valid."""
        user_id = validate_user(email.data, form.password.data)
        if not user_id:
            #User with given credentials does not exist, raise a validation error
            raise ValidationError("Invalid email or password.")
def verify_username_in_use(form, username):
    """Custom field validator that check if username is already in-use."""
    if check_username_exists(username.data):
        #User already exists, raise a validation error
        raise ValidationError(f"Username {username.data} already in-use.")

class LoginForm(Form):
    email = EmailField('Email', [validators.Length(min=4, max=50),
                                 check_credentials])
    password = PasswordField('Password', [validators.Length(min=4, max=35,
                                    message="Password must be minimum of 8 characters.")])

class RegisterForm(Form):
    email = EmailField('Email', [validators.Length(min=4, max=50),
                                verify_email_in_use])
    username = StringField('Username', [validators.Length(min=4, max=25, 
                                        message="Username must be between 4 and 25 characters."),
                                        verify_username_in_use])
    password = PasswordField('Password', [validators.Length(min=8, max=35)])

    confirm_password = PasswordField('Confirm Password', [validators.Length(min=8, max=35,
                                    message="Password must be minimum of 8 characters."),
                                                 validators.EqualTo('password', message='Passwords do not match.')])
    

class NewPostForm(Form):
    title = StringField('Title', [validators.Length(min=4, max=100, 
                                message="Title must be between 4 and 100 characters."),
                                validators.DataRequired(message="Title is required.")])
    
    content = TextAreaField('Content', [validators.Length(min=4, max=1000, 
                                        message="Content must be between 4 and 1000 characters."),
                                        validators.DataRequired(message="Content is required.")])
    
    excerpt = TextAreaField('Excerpt', [validators.Length(min=4, max=200,
                                        message="Excerpt must be between 4 and 200 characters."),
                                        validators.DataRequired(message="Excerpt is required.")])
    
    tag = StringField('Tag', [validators.Length(min=4, max=100, 
                                        message="Tag must be between 4 and 100 characters.")])

class FilterPostsForm(Form):
    tag = StringField('Tag', [validators.Length(max=100)])
    username = StringField("Author's username", [validators.Length(max=50)])
    title = StringField('Title', [validators.Length(max=50)])

def register_form(formdata=None):
    return RegisterForm(formdata)

def login_form(formdata=None):
    return LoginForm(formdata)

def new_post_form(formdata=None):
    return NewPostForm(formdata)

def filter_posts_form(formdata=None):
    return FilterPostsForm(formdata)
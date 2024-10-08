"""When executed, this script will generate mock users and mock posts in the database."""

from .mock_posts import generate_posts
from .mock_users import generate_users

generate_users()
generate_posts()

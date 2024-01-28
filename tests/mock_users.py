"""Generates mock users for testing purposes."""

from faker import Faker
from app.dbschema import User, ENGINE
from app.util import password_hash
from sqlalchemy.orm import Session


def generate_users(quantity=5) -> None:
    """Generates mock users for testing purposes."""
    fake = Faker()
    with Session(ENGINE) as session:
        for _ in range(quantity):
            profile = fake.simple_profile()
            user = User(username=profile["username"],
                        email=profile["mail"],
                        password_hash=password_hash("password"))
            session.add(user)
        session.commit()
    
if __name__ == "__main__":
    generate_users()
"""Generates mock users for testing purposes."""
#pylint: disable=import-error
from faker import Faker
from sqlalchemy.orm import Session
from app.dbschema import User, ENGINE
from app.util import password_hash

def generate_users(quantity=5) -> None:
    """Generates mock users for testing purposes."""
    fake = Faker()
    with Session(ENGINE) as session:
        for _ in range(quantity):
            #Add random mock users
            profile = fake.simple_profile()
            user = User(username=profile["username"],
                        email=profile["mail"],
                        password_hash=password_hash("password"))
            session.add(user)
        #Add admin user
        user = User(username="admin",
                    email="admin@blog.com",
                    password_hash=password_hash("password"),
                    admin=True)
        session.add(user)
        session.commit()

if __name__ == "__main__":
    generate_users()

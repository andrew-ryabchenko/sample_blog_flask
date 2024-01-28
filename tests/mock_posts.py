"""Generates mock posts for testing purposes."""

from faker import Faker
from app.dbschema import Post, User, ENGINE
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime as dt

def generate_posts(ppu=5) -> None:
    """Generates posts for each user in the database."""
    fake = Faker()
    with Session(ENGINE) as session:
        users = session.execute(select(User)).all()
        for user in users:
            for _ in range(ppu):
                timestamp = dt.now().strftime("%m/%d/%Y, %H:%M")
                title = fake.sentence()
                excerpt = fake.text(max_nb_chars=200)
                content = fake.text(max_nb_chars=1000)
                tag = fake.word().capitalize()
                user_id = user[0].id
                post = Post(title=title,
                            excerpt=excerpt,
                            content=content,
                            tag=tag,
                            timestamp=timestamp,
                            user_id=user_id)
                session.add(post)
        
        session.commit()

if __name__ == "__main__":  
    generate_posts()
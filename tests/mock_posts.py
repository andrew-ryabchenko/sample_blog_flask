"""Generates mock posts for testing purposes."""
#pylint: disable=import-error
from datetime import datetime as dt
from faker import Faker
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.dbschema import Post, User, ENGINE

def generate_posts(ppu=5) -> None:
    """Generates posts for each user in the database."""
    fake = Faker()
    username_post_mapping = {}
    tag_post_mapping = {}
    title_post_mapping = {}
    with Session(ENGINE) as session:
        users = session.execute(select(User)).all()
        for user in users:
            for _ in range(ppu):
                timestamp = dt.now().strftime("%m/%d/%Y, %H:%M")
                title = fake.sentence()
                excerpt = fake.text(max_nb_chars=200)
                content = fake.text(max_nb_chars=1000)
                tag = fake.text(max_nb_chars=30)
                user_id = user[0].id
                post = Post(title=title,
                            excerpt=excerpt,
                            content=content,
                            tag=tag,
                            timestamp=timestamp,
                            user_id=user_id)
                if user[0].username not in username_post_mapping:
                    username_post_mapping[user[0].username] = []
                    username_post_mapping[user[0].username].append(post)
                else:
                    username_post_mapping[user[0].username].append(post)

                if tag not in tag_post_mapping:
                    tag_post_mapping[tag] = []
                    tag_post_mapping[tag].append(post)
                else:
                    tag_post_mapping[tag].append(post)

                if title not in title_post_mapping:
                    title_post_mapping[title] = []
                    title_post_mapping[title].append(post)
                else:
                    title_post_mapping[title].append(post)

                session.add(post)
        session.commit()

    return (username_post_mapping, tag_post_mapping, title_post_mapping)

if __name__ == "__main__":
    generate_posts()

from app.models import add_user
from sqlalchemy.orm import object_session

#Add demo admin user to the database
user = add_user("admin@blog.com", "admin", "admin", admin=True)
session = object_session(user)
session.commit()
session.close()
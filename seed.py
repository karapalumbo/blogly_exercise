from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
alan_alda = User(first_name='Alan', last_name="Alda")
joel_burton = User(first_name='Joel', last_name="Burton")
jane_smith = User(first_name='Jane', last_name="Smith")

# Add posts
alan_alda_post = Post(title='Post 1', content="Hello there!", created_at="2020-10-10", fk=1)
joel_burton_post = Post(title='First post', content="This is my first post!", created_at="2021-1-1", fk=2)
jane_smith_post = Post(title='My post', content="First post!", created_at="2020-11-11", fk=3)

db.session.add_all([alan_alda, joel_burton, jane_smith, alan_alda_post, joel_burton_post, jane_smith_post])

db.session.commit()

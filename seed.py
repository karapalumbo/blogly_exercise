# from models import User, Post, Tag, PostTag, db
# from app import app

# # Create all tables
# db.drop_all()
# db.create_all()

# # If table isn't empty, empty it
# User.query.delete()

# # Add users
# alan_alda = User(first_name='Alan', last_name="Alda")
# joel_burton = User(first_name='Joel', last_name="Burton")
# jane_smith = User(first_name='Jane', last_name="Smith")

# # Add posts
# alan_alda_post = Post(title='Post 1', content="Hello there!", created_at="2020-10-10", fk=alan_alda.id)
# joel_burton_post = Post(title='First post', content="This is my first post!", created_at="2021-1-1", fk=joel_burton.id)
# jane_smith_post = Post(title='My post', content="First post!", created_at="2020-11-11", fk=jane_smith.id)

# db.session.add_all([alan_alda, joel_burton, jane_smith, alan_alda_post, joel_burton_post, jane_smith_post])

# db.session.commit()


# # Add tags 
# alan_alda_tags = Tag(name='Fun', post=[PostTag(post_id=alan_alda_post.id, tag_id=alan_alda_tags.id)])
# joel_burton_tags = Tag(name='Even More', post=[PostTag(post_id=joel_burton_post.id, tag_id=joel_burton_tags.id)])
# jane_smith_tags = Tag(name='Yass', post=[PostTag(post_id=jane_smith_post.id, tag_id=jane_smith_tags.id)])



# # db.session.add_all([alan_alda, joel_burton, jane_smith, alan_alda_post, joel_burton_post, jane_smith_post, alan_alda_tags, joel_burton_tags, jane_smith_tags])

# # db.session.commit()



# db.session.add_all([alan_alda_tags, joel_burton_tags, jane_smith_tags])

# db.session.commit()

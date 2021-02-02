from unittest import TestCase
from app import app
from models import db, User, Post
from flask import redirect

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class FlaskTests(TestCase):

    def setUp(self):

        User.query.delete()

        user = User(first_name="John", last_name="Smith")
        post = Post(title="Food", content="Food is amazing", created_at="2021/1/2", fk=1)
        db.session.add(user)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        self.post_id = post.id
        self.post = post

    def tearDown(self):

        db.session.rollback()


    def test_homepage(self):
        """ Testing homepage and redirect """
        with app.test_client() as client:
            response = client.get('/', follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('John', html)


    def test_show_user(self):
        """testing list of users page"""
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
    
    def test_create_user(self):
        """testing if new user gets added"""
        with app.test_client() as client:
            d = {"fname": "John", "lname": "Smith", "image":"image"}
            response = client.post('/users/new', data=d, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("John", html)

    
    def test_update_user(self):
        """testing if user is updated"""
        with app.test_client() as client: 
            d = {"fname": "Pablo", "lname": "Smith", "image":"image"}
            response = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn("Pablo", html)


    def test_show_posts(self):
        """testing list of posts page"""
        with app.test_client() as client:
            response = client.get(f"/users/{self.user_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h2>Posts</h2>', html)


    def test_update_post(self):
        """testing post"""
        with app.test_client() as client: 
            d = {"title": "First Post", "content": "This is my first post"}
            response = client.post(f"/posts/{self.post.id}/edit", data=d, follow_redirects=True)
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn("<h1>First Post</h1>", html)


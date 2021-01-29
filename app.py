"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "seeecret"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route('/')
def list_users():

    return redirect('/users')


@app.route('/users')
def show_users_link():
    users = User.query.all()
    return render_template("base.html", users=users)


@app.route('/users/new')
def new_user_form():
    return render_template("new_users.html")


@app.route('/users/new', methods=["POST"])
def create_user():
    fname = request.form["fname"]
    lname = request.form["lname"]
    image = request.form["image"]
    image = "" if image else None

    new_user = User(first_name=fname, last_name=lname, image_url=image)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["fname"]
    user.last_name = request.form["lname"]
    user.image_url = request.form["image"]

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route("/users/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

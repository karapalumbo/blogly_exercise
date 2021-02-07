"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
def homepage():
    # """ homepage """
    return redirect('/users')

@app.route('/users')
def show_users_link():
    # """ show users """
    users = User.query.all()
    return render_template("base.html", users=users)


@app.route('/users/new')
def new_user_form():
    # """ show new user form """
    return render_template("new_users.html")


@app.route('/users/new', methods=["POST"])
def create_user():
    # """ add new user """
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
    # """ show details of certain user """
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    # """ show edit user form """
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=['POST'])
def update_user(user_id):
    # """ edit user """
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["fname"]
    user.last_name = request.form["lname"]
    user.image_url = request.form["image"]

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route("/users/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):
    # """ delete user """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    # """ show new post form """
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("post_form.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=['POST'])
def add_post(user_id):
    # """ create/ add new post """
    user = User.query.get_or_404(user_id)
    # tags = Tag.query.all()
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'], content=request.form['content'], user=user, tags=tags)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    # """ show posts for each user """
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('show_posts.html', post=post, tags=tags)

    
@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    # """ show edit post form """
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template("edit_post.html", post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def submit_edit_post(post_id):
    # """ edit post """
    post = Post.query.get_or_404(post_id)
    
    post.title = request.form["title"]
    post.content = request.form["content"]

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    # """ delete post """
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect("/users")


@app.route('/tags')
def list_tags():
    # """ list all tags """
    tags = Tag.query.all()
    return render_template("tag_list.html", tags=tags)


@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    # """ shows tag details """
    tags = Tag.query.get_or_404(tag_id)
    post = Post.query.all()

    return render_template("tag_detail.html", tags=tags, post=post)


@app.route('/tags/new')
def add_tag():
    # """ tag form """
    tags = Tag.query.all()
    post = Post.query.all()
    return render_template("new_tag.html", tags=tags, post=post)


@app.route('/tags/new', methods=['POST'])
def submit_tag():
    # """ submit tag form """

    # post = Post.query.all()
    post_ids = [int(num) for num in request.form.getlist("post")]
    post = Post.query.filter(Post.id.in_(post_ids)).all()
 
    new_tag = Tag(name=request.form['tag_name'], post=post)
    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    # """ show edit tag form"""
    tags = Tag.query.get_or_404(tag_id)
    
    return render_template("edit_tag.html", tags=tags)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def submit_edit_tag(tag_id):
    # """ edit tags """
    tags = Tag.query.get_or_404(tag_id)
    tags.name = request.form["tag_name"]

    post_ids = [int(num) for num in request.form.getlist("post")]
    tags.post = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tags)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    # """ delete tag """
    tags = Tag.query.get_or_404(tag_id)

    db.session.delete(tags)
    db.session.commit()

    return redirect("/tags")
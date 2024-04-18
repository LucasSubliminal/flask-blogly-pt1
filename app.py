"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import DEFAULT_IMAGE, db, connect_db, User, Post, Tag
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'thisisthesecretkey'

toolbar = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def list_names():
    """ Brings users to the home page which is a list of users """
    
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/home.html', title="Users", users=users)

@app.route('/users/new', )
def create_user():
    """ Redirects users to the create users form """

    return render_template('users/createusers.html', title="Create a User")


@app.route('/users/<int:user_id>')
def user_detail_page(user_id):
    """  Returns the detail page for each specific user """ 
    #Request full name from database and put it in the title 
    users = User.query.order_by(User.last_name, User.first_name).all()
    user = User.query.get(user_id)
    img_url = user.image_url
    id_user= User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.title).all()


    return render_template('users/userdetailpage.html', users = users, img_url=img_url, id_user=id_user, user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_profile(user_id):
    """ Returns the edit profile page for each specific user """

    user = User.query.get(user_id)
    first = user.first_name
    last = user.last_name
    img_url = user.image_url
    return render_template('users/editusers.html', title="Edit a user", first=first, last=last, img_url=img_url)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle form submission for creating a new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")

@app.route('/users/<int:user_id>/posts/new')
def add_post(user_id):
    """Returns page to add a new post for specific user """
    user = User.query.get(user_id)
    full_name = user.full_name 
    return render_template('users/newposts.html', title=f"Add Post for {full_name}", user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']
    created_at = datetime.utcnow()

    new_post = Post(title=title, content=content, created_at=created_at, user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added successfully.")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def  show_post(post_id):
    """ Show posts page"""
    post = Post.query.get_or_404(post_id)
    content = post.content
    user = post.user
    full_name= user.full_name

    return render_template('users/postpage.html', title='First Post!', content=content, user=user, full_name=full_name, post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_posts(post_id):
    """ Edits posts """
    post = Post.query.get(post_id)

    return render_template('users/editpost.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    post = Post.query.get_or_404(post_id)

    title = request.form.get('title', 'No Title Provided')
    content = request.form.get('content', 'No Content Provided')

    if title and content: 
        post.title = title
        post.content = content
        db.session.commit()
        flash(f"Post '{post.title}' edited successfully.")
    else:
        flash("Error: Title and content are required.")

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")



@app.route('/tags')
def tags_index():
    """Show a page with info on all tags"""

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """Show a form to create a new tag"""

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")





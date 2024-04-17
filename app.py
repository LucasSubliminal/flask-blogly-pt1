"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

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

@app.route('/createusers')
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



    return render_template('users/userdetailpage.html', users = users, img_url=img_url, id_user=id_user, user=user)

@app.route('/users/editpage/<int:user_id>')
def edit_profile(user_id):
    """ Returns the edit profile page for each specific user """

    user = User.query.get(user_id)
    first = user.first_name
    last = user.last_name
    img_url = user.image_url
    return render_template('users/editusers.html', title="Edit a user", first=first, last=last, img_url=img_url)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

DEFAULT_IMAGE = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

class User(db.Model):
    """ Apps User """

    __tablename__ = 'users'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                           nullable=False,
                           )
    last_name = db.Column(db.Text,
                           nullable=False,
                           )
    image_url = db.Column(db.Text,
                          nullable=False,
                          default=DEFAULT_IMAGE
                          )
    posts = db.relationship('Post', backref='user')  # Relationship defined here

    @property
    def full_name(self):
        """Users full name"""
        
        return f"{self.first_name} {self.last_name}"
    
def connect_db(app):
    """ Connect database in Flask App """

    db.app = app
    db.init_app(app)

class Post(db.Model):
    """Blog posts"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True
                   )
    title = db.Column(db.Text,
                      nullable=False
                      )
    content = db.Column(db.Text,
                        nullable=False
                        )
    created_at = db.Column(db.Date,
                           nullable=False
                           )
    user_id = db.Column(db.Integer,
                            db.ForeignKey('users.id'),
                            nullable=False
                            )

    
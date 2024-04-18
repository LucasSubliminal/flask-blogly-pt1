"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

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
    posts = db.relationship('Post', backref='user')  

    @property
    def full_name(self):
        """Users full name"""
        
        return f"{self.first_name} {self.last_name}"
    
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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Correct usage


                        
    user_id = db.Column(db.Integer,
                            db.ForeignKey('users.id'),
                            nullable=False
                            )

class PostTag(db.Model):
    """Tags id and Posts id together"""

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True
                        )
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True
                       )

class Tag(db.Model):
    """ Tags for the posts """

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                    nullable=False, 
                    unique=True
                    )
    posts = db.relationship(
        'Post',
        secondary='post_tags',
        backref='tags'
    )
                     
def connect_db(app):
    """ Connect database in Flask App """

    db.app = app
    db.init_app(app)
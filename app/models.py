from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy() # initializes database

# create our Models
# db.Models gives us ability to work with database
# UserMixin helps keep track of who is logged in
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    team = db.relationship("Team", backref='trainer', lazy=True) #backref, from the team it will look and see who the trainer/user is

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon1 = db.Column(db.String(60))
    pokemon2 = db.Column(db.String(60))
    pokemon3 = db.Column(db.String(60))
    pokemon4 = db.Column(db.String(60))
    pokemon5 = db.Column(db.String(60))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, user_id):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.pokemon3 = pokemon3
        self.pokemon4 = pokemon4
        self.pokemon5 = pokemon5
        self.user_id = user_id
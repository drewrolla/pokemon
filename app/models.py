from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy() # initializes database

# links Pokemon to User
user_pokemon = db.Table('user_pokemon',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'))
)

battling = db.Table('battling',
    db.Column('battling_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('battler_id', db.Integer, db.ForeignKey('user.id'))
)

# create our Models
# db.Models gives us ability to work with database
# UserMixin helps keep track of who is logged in
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)
    team = db.relationship("Team", backref='trainer', lazy=True) #backref, from the team it will look and see who the trainer/user is
    team = db.relationship("Pokemon",
        secondary = user_pokemon,
        backref = 'trainers',
        lazy = 'dynamic'
    )
    fight = db.relationship("User",
        primaryjoin = (battling.c.battling_id==id),
        secondaryjoin = (battling.c.battler_id==id),
        secondary = battling,
        backref = 'fighters',
        lazy = 'dynamic'
    )

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def fightUser(self, user):
        self.fight.append(user)
        db.session.commit()

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    ability = db.Column(db.String)
    img_url = db.Column(db.String)
    hp = db.Column(db.String)
    attack = db.Column(db.String)
    defense = db.Column(db.String)

    def __init__(self, name, ability, img_url, hp, attack, defense):
        self.name = name
        self.ability = ability
        self.img_url = img_url
        self.hp = hp
        self.attack = attack
        self.defense = defense
    
    def save(self):
        db.session.add(self)
        db.session.commit()


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

    def updateTeam(self, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.pokemon3 = pokemon3
        self.pokemon4 = pokemon4
        self.pokemon5 = pokemon5

    def save(self):
        db.session.add(self)
        db.session.commit()

    def saveUpdates(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
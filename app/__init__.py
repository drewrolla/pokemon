from flask import Flask
from config import Config
from flask_login import LoginManager

# import Blueprints
from .auth.routes import auth
from .poke.routes import poke
from .models import User

app = Flask(__name__)
login = LoginManager()

@login.user_loader # function creates variable called current_user which can be used anywhere within this app
def load_user(user_id):
    return User.query.get(user_id)

# register Blueprints
app.register_blueprint(auth)
app.register_blueprint(poke)

app.config.from_object(Config)

# intiialize our database to work with our app
from .models import db
from flask_migrate import Migrate

# initializes db
db.init_app(app)
migrate = Migrate(app, db)
login.init_app(app)

login.login_view = 'auth.logMeIn'

from . import routes # this should always be at the bottom, otherwise it will throw a circular loop
from . import models
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import LoginForm, UserCreationForm # goes into .forms (in auth folder) and gets the form
from werkzeug.security import check_password_hash

# import login functionality
from flask_login import login_user, logout_user, login_required, current_user

# import Models
from app.models import User, db

auth=Blueprint('auth', __name__, template_folder='authtemplates')

@auth.route('/login', methods=["GET", "POST"])
def logMeIn():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            # query user based off of username
            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Log in successful.', 'success')
                    login_user(user)
                    return redirect(url_for('poke.showTeamPage'))
            else:
                flash('Incorrect password', 'danger')
            # if user does not exist
        else:
            flash('Account does not exist.', 'danger')
    return render_template('login.html', form=form)


@auth.route('/logout', methods=["GET", "POST"])
def logMeOut():
    flash("You've yee'd your last haw.", 'success')
    logout_user()
    return redirect(url_for('auth.logMeIn'))



@auth.route('/signup', methods=["GET", "POST"])
def SignMeUp():
    form = UserCreationForm()
    if request.method == "POST": # if the request is a POST (meaning submit form info), do all the stuff within that code block - fill in form, validate info, and then add to db
        print('POST req made')
        if form.validate(): # if form validates, it will grab the following info
            username = form.username.data
            email = form.email.data
            password = form.password.data

            # add user to db
            user = User(username, email, password)

            # store to db/add instance
            db.session.add(user)
            db.session.commit()

            flash('Account created.', 'success')
            return redirect(url_for('auth.logMeIn')) # redirects user to the url for the function logMeIn
        else:
            flash('Invalid input. Please try again.', 'danger')
    else:
        print('GET req made') # if request is GET, it will return the webpage itself
    return render_template('signup.html', form=form)

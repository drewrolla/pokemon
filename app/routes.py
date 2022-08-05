from app import app # says, from the app folder import the app module (app=Flask(__name__))
from flask import render_template


@app.route('/') # when you declare a route, the function under it will run!
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

# class notes
# def index():
#     staff = [{'name': 'andrew', 'img': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/SNice.svg/800px-SNice.svg.png', 'age': '9000'}, {'name': 'wesley', 'img': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/SNice.svg/800px-SNice.svg.png', 'age': '9001'}, {'name': 'whiskey', 'img': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/SNice.svg/800px-SNice.svg.png', 'age': '9002'}]
#     return render_template('index.html', names=staff, )
# you can rename called lists in the return function, and it will use the list by that name
# *args means you can pass in an infinite num of arguments
# **kwargs means you can pass in an infinite num of keyword arguments

@app.route('/contact')
def contact():
    return render_template('contact.html')

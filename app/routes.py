from flask import render_template, redirect, url_for, session
from app import app, db
from app.models import User, Post

@app.route("/")
def index():
    #to_return = "<img src='/static/images/stars.jpg' alt='no image found'>"
    #image_url = url_for('memes', filename='spongebob-leak.gif')
    image_url = '/memes/spongebob-leak.gif'
    to_return = "<img src='%s' alt='no image found!!'>" % (image_url)
    session_user = dict(session).get('user', None)
    if (session_user):
        to_return = to_return + "<p>User {} is logged in</p>".format(session_user["userinfo"]["name"])
    return '<p>This is a Python Flask app running with Gunicorn and Nginx! 🐍+🧪+🦄+🚙 = ⚡️💪🔥</p>' + to_return + image_url

@app.route("/home")
def home():
    # Testing
    # u = User(username='john', email='john@example.com')
    # assert not (u == None)
    # db.session.add(u)
    # db.session.commit()
    users = User.query.all()
    assert not (users == None)
    # End Testing
    return render_template("home.html", session=dict(session).get('user', None), users=users) 
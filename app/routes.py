import sys
from flask import request, render_template, redirect, url_for, session
from app import app, db
from app.models import User, Post, admins, liked_posts, disliked_posts
import json
import requests
from sqlalchemy import select, or_, insert, delete, update
import sqlalchemy
from flask_caching import Cache
import httpx
import asyncio
import ast

cache = Cache(app)

base_url = 'https://hacker-news.firebaseio.com/v0/'

import datetime

@app.route("/")
def index():
    return render_template("land.html")
    
@app.route("/home")
def home():
    uid = get_user_id()
    posts = get_posts()
    liked_posts = get_voted_posts(uid, vote_type="like")
    disliked_posts = get_voted_posts(uid, vote_type="dislike")
    current_time = datetime.datetime.now()
    for post in posts:
        time_posted = datetime.datetime.fromtimestamp(post['time'])
        time_since = current_time - time_posted
        hours, rem = divmod(time_since.seconds, 3600)
        post['time'] = hours
    sys.stdout.flush()
    return render_template(
        "home.html",
        session=dict(session).get('user', None),
        posts=posts, isadmin=isadmin(uid),
        liked_posts=liked_posts, disliked_posts=disliked_posts
        )


def get_posts():
    with requests.Session() as s:
        top = s.get(base_url + "topstories.json").json()
        stories = [get_story_json(story_id, s) for story_id in top[0:100]]
        return stories

def get_story_json(story_id, s):
    @cache.memoize(timeout=604800) # one week
    def inner_get_json(story_id):
        extension = "item/" + str(story_id) + ".json"
        new_response = s.get(base_url + extension)
        return new_response.json()
    return inner_get_json(story_id)

def get_voted_posts(uid, vote_type):
    stmt = ""
    res = ""
    if vote_type == "dislike":
        stmt = select(disliked_posts).where(disliked_posts.c.user_id==uid)
        res = db.session.execute(stmt).all()
    elif vote_type == "like":
        stmt = select(liked_posts).where(liked_posts.c.user_id==uid)
        res = db.session.execute(stmt).all()

    res = [i[1] for i in res]
    print((res))
    print(type(res))
    sys.stdout.flush()

    return res

async def get_posts_async():
    async with httpx.AsyncClient() as s:
        top = (await s.get(base_url + 'topstories.json')).json()
        tasks = [
            s.get(base_url+'/item/'+str(article)+'.json')
            for article in top[0:10]
        ]
        posts = await asyncio.gather(*tasks)
        posts = [story.json() for story in posts]
        return posts

def isadmin(user_id):
    try:
        stmt = select(admins).where(admins.c.user_id == user_id)
        admin = db.session.execute(stmt).first()
        print(admin)
        sys.stdout.flush()
        return admin != None
    except Exception as e:
        print(e)
        return False

@app.route("/about")
def about():
    return render_template("about.html")

def get_user_id():
    users = []
    uid = -1
    try:
        uinfo = dict(session).get('user', None)
        uinfo = dict(uinfo).get('userinfo', None)
        stmt = select(User.id).where(User.email == uinfo['email'])
        try:
            users = db.session.execute(stmt).first()
            uid = users._asdict()['id']
            parsed = json.dumps((session), indent=4) 
            return uid
        except Exception as e:
            print("Error in db access")
    except Exception as e:
        print(e)
        print("Error in user session")

def vote(vote_type):

    uid = get_user_id()
    story_id = ""
    if request.method == 'POST':
        story_id = request.form[vote_type]
    
    story = {}
    with requests.Session() as s:
        story = get_story_json(story_id, s)
        newpost = Post(
            id=story['id'],
            post_type=story['type'],
            by=story['by'],
            title=story['title'],
            url=story.get('url', '')
        )
        try:
            db.session.add(newpost)
            print('test')
        except Exception as e:
            db.session.rollback()
        else:
            try:
                db.session.commit()
            except:
                db.session.rollback()
                print("Integrity error")

    stmt = select(Post).where(Post.id==story['id'])
    mypost = db.session.execute(stmt).first()
    mypost = str(mypost[0])
    mypost = (ast.literal_eval(mypost))
    if vote_type == "dislike":
        stmt = (
            insert(disliked_posts).
            values(user_id=uid, post_id=mypost['id'])
        )
    elif vote_type == "like":
        stmt = (
            insert(liked_posts).
            values(user_id=uid, post_id=mypost['id'])
        )

    try:
        db.session.execute(stmt)
        db.session.commit()
    except Exception as e:
        print("Except")


@app.route("/dislike", methods = ['POST'])
def dislike():
    vote("dislike")
    return redirect(request.referrer)

@app.route("/like", methods = ['POST'])
def like():
    vote("like")
    return redirect(request.referrer)

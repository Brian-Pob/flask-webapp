import sys
from flask import render_template, redirect, url_for, session
from app import app, db
from app.models import User, Post, admins
import json
import requests
from sqlalchemy import select, or_

from flask_caching import Cache
import httpx
import asyncio

cache = Cache(app)

base_url = 'https://hacker-news.firebaseio.com/v0/'

import datetime

@app.route("/")
def index():
    return render_template("land.html")
    
@app.route("/home")
def home():
    users = []
    uid = -1
    try:
        uinfo = dict(session).get('user', None)
        uinfo = dict(uinfo).get('userinfo', None)
        stmt = select(User.id).where(User.email == uinfo['email'])
        try:
            users = db.session.execute(stmt).first() 
            print(type(users))
            print((users._asdict()))
            uid = users._asdict()['id']
            parsed = json.dumps((session), indent=4) 
        except Exception as e:
            print("Error in db access")
    except Exception as e:
        print(e)
        print("Error in user session")
    posts = get_posts()
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
        users=users, posts=posts, isadmin=isadmin(uid))


def get_posts():
    with requests.Session() as s:
        
        @cache.memoize(timeout=604800) # one week
        def get_story_json(story_id):
            extension = "item/" + str(story_id) + ".json"
            new_response = s.get(base_url + extension)
            return new_response.json()

        top = s.get(base_url + "topstories.json").json()
        stories = [get_story_json(story_id) for story_id in top[0:100]]
        return stories


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


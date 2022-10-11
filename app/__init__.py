from os import environ as env
from dotenv import find_dotenv, load_dotenv
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 
from config import Config 
from authlib.integrations.flask_client import OAuth


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
    
app.secret_key = env.get("APP_SECRET_KEY")

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

from app.auth import auth_bp 
app.register_blueprint(auth_bp)

from app import routes, models

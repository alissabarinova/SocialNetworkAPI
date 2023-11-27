from flask import Flask

app = Flask(__name__)

USERS = {}  # dict for objects type User
POSTS = {}  # dict for objects type Post
EMAILS = []  # list for user's email

from app import main_route
from app import views
from app import models
from app import tests

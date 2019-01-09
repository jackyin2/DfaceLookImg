from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os


app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Tunicorn@hf#2017@172.16.1.6:3306/dface_community"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config['SECRET_KEY'] = '1f31472e4e774f00865b6ca0c5cc08d8'
# app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")

db = SQLAlchemy(app)
from app import blueview
from app import filter_utils

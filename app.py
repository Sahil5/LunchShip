import jinja2
from flask import Flask, session, flash, redirect, url_for, request, get_flashed_messages, jsonify, render_template
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user
from flask.ext.sqlalchemy import SQLAlchemy

from flask import Flask, request
from flask import render_template
import secrets

from helpers.forms import CreateLunchShip, LoginForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = secrets.DB_CONN_STRING
app.secret_key = secrets.SECRET_KEY
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

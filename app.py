import jinja2
from flask import Flask, session, flash, redirect, url_for, request, get_flashed_messages, jsonify, render_template
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user

from flask import Flask, request
from flask import render_template
import secrets

from helpers.forms import CreateLunchShip


app = Flask(__name__)
app.secret_key = secrets.SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)

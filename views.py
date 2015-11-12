from app import app
from flask import flash, redirect, url_for, request, render_template
from flask.ext.login import current_user, login_user, logout_user
from auth import check_auth, requires_login, User
from helpers.forms import CreateLunchShip


@app.route('/login', methods=['post'])
def login():
    username = request.form['username']
    password = request.form['password']
    if check_auth(username, password):
        login_user(User(username))
    else:
        flash('Username or password incorrect')

    return redirect(url_for('index'))


@app.route("/")
@requires_login
def index():
    return redirect(url_for('create_new_ship'))


@app.route("/new_ship", methods=['GET', 'POST'])
@requires_login
def create_new_ship():
    lunch_ship_form = CreateLunchShip(request.form)
    if request.method == 'POST' and lunch_ship_form.validate():
        pass

    return render_template(
        "home.html",
        lunch_ship_form=lunch_ship_form
    )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

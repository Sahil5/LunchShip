from app import app
from flask import flash, redirect, url_for, request, render_template, session
from flask.ext.login import current_user, login_user, logout_user
from auth import check_auth, requires_login, User
from helpers.forms import CreateLunchShip, LoginForm


@app.route("/")
def index():
    if current_user.is_authenticated:
        username = current_user.get_id()
        session['username'] = username

        return redirect(url_for('create_new_ship'))

    login_form = LoginForm(request.form)

    return render_template(
        "login.html",
        login_form=login_form
    )

@app.route("/new_ship", methods=['GET', 'POST'])
def create_new_ship():
    lunch_ship_form = CreateLunchShip(request.form)

    if request.method == 'POST' and lunch_ship_form.validate():
        return render_template("new_ships.html")

    return render_template(
        "home.html",
        lunch_ship_form=lunch_ship_form
    )

@app.route('/login', methods=['post'])
def login():
    username = request.form['username']
    password = request.form['password']

    login_form = LoginForm(request.form)

    if login_form.validate():
        if check_auth(username, password):
            login_user(User(username))
        else:
            flash('Wrong username or password')
    else:
        flash('Please fill out all fields')

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
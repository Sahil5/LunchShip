import datetime

from app import app
from flask import flash, redirect, url_for, request, render_template, session
from flask.ext.login import current_user, login_user, logout_user
from auth import check_auth, requires_login, User, show_login, require_login
from helpers.forms import LoginForm, AddShip
from helpers.view import user_form_handler

from logic import create_ship
from presentation.ships import get_all_lunch_ship_presenters


@app.route("/")
@requires_login
def index():
    return redirect(url_for('show_all_ships'))


def add_ship_db(username, form):
    create_ship(
        username,
        form.destination.data,
        datetime.datetime.combine(
            datetime.date.today(),
            form.departure_time.data,
        ),
    )


create_new_ship = user_form_handler(
    AddShip,
    "home.html",
    lambda form: form.captain.data,
    add_ship_db,
    'show_all_ships',
)


@app.route('/ship/add', methods=['GET', 'POST'])
def add_ship():
    return create_new_ship()


@app.route('/ships/all')
@requires_login
def show_all_ships():
    lunch_ship_presenters = get_all_lunch_ship_presenters()

    # TODO: Add logic for deciding on which projects a person is captain of
    is_captain = True

    return render_template(
        "all_ships.html",
        lunch_ship_presenters=lunch_ship_presenters,
        is_captain=is_captain,
    )


@app.route('/ship/<int:ship_id>/join')
@requires_login
def join_ship(ship_id):
    # TODO: add logic for joining ship
    flash('You have just joined a new ship')

    return redirect(url_for('show_all_ships'))


@app.route('/ship/<int:ship_id>/join')
@requires_login
def edit_ship(ship_id):
    return render_template("edit_ship.html")


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

import datetime

from app import app
from flask import flash, redirect, url_for, request, render_template
from flask.ext.login import current_user, login_user, logout_user
from auth import check_auth, requires_login, User, show_login, require_login
from helpers.forms import LoginForm, AddShip
from helpers.view import user_form_handler

from logic import create_ship
from logic import get_all_sailing_ships


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


@app.route('/ship/add', methods=['GET'])
@requires_login
def add_ship():
    return render_template(
        'home.html',
        form=AddShip(request.form),
    )

@app.route('/ship/add', methods=['POST'])
def add_ship_post():
    return create_new_ship()


@app.route('/ships/all')
@requires_login
def show_all_ships():
    return render_template(
        "all_ships.html",
        sailing_ships=get_all_sailing_ships(),
    )


@app.route('/ship/<int:ship_id>/join')
@requires_login
def join_ship(ship_id):
    # TODO: add logic for joining ship
    flash('You have just joined a new ship')

    return redirect(url_for('show_all_ships'))


@app.route('/ship/<int:ship_id>/edit')
@requires_login
def edit_ship(ship_id):
    return render_template("edit_ship.html")


@app.route('/login', methods=['post'])
def login():
    login_form = LoginForm(request.form)

    if login_form.validate():
        if check_auth(
            login_form.username.data,
            login_form.password.data,
        ):
            login_user(User(login_form.username.data))
        else:
            flash('Wrong username or password')
    else:
        flash('Please fill out all fields')

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

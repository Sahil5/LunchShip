import datetime

from app import app
from flask import flash, redirect, url_for, request, render_template, jsonify
from flask.ext.login import current_user, login_user, logout_user
from auth import check_auth, requires_login, User, render_login
from helpers.forms import LoginForm, AddShip, JoinShip
from helpers.view import handle_user_form

from logic import create_ship
from logic import join_lunch_ship
from logic import get_all_sailing_ships


@app.route("/")
@requires_login
def index():
    return redirect(url_for('show_all_ships'))


@app.route('/ship/add', methods=['GET'])
@requires_login
def add_ship():
    return render_template(
        'home.html',
        form=AddShip(request.form),
    )


@app.route('/ship/add', methods=['POST'])
def add_ship_post():
    def on_success(username, form):
        create_ship(
            username,
            form.destination.data,
            datetime.datetime.combine(
                datetime.date.today(),
                form.departure_time.data,
            ),
        )
    return handle_user_form(
        AddShip(request.form),
        "home.html",
        on_success,
        'show_all_ships',
    )


@app.route('/ships/all')
@requires_login
def show_all_ships():
    return render_template(
        "all_ships.html",
        sailing_ships=get_all_sailing_ships(),
    )


@app.route('/ships/all/json', methods=['POST'])
def all_ships_json():
    ships = get_all_sailing_ships()
    return jsonify(
        ships=[
            {
                'id': ship.id,
                'captain_id': ship.captain_id,
                'destination': ship.destination,
                'time_created': str(ship.time_created),
                'depature_time': str(ship.departure_time),
            } for ship in ships
        ],
    )


@app.route('/ship/<int:ship_id>/join', methods=['GET', 'POST'])
def join_ship_post(ship_id):
    def on_success(username, form, ship_id):
        flash('You have just joined ship %d' % ship_id)
        join_lunch_ship(
            ship_id,
            username,
        )

    return handle_user_form(
        JoinShip(request.form),
        show_all_ships,
        on_success,
        'show_all_ships',
        ship_id,
    )


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

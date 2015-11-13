import datetime
from app import app
from flask import flash, redirect, url_for, request, render_template
from flask.ext.login import current_user, login_user, logout_user
from auth import check_auth, requires_login, User, show_login, require_login
from helpers.forms import LoginForm, AddShip, EditShip
from helpers.view import user_form_handler

from logic import create_ship
from logic import join_lunch_ship
from logic import get_all_sailing_ships
from logic import get_ship_by_id
from logic import edit_ship_by_id


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
    flash('You have just joined ship %d' % ship_id)
    join_lunch_ship(
        ship_id,
        current_user.get_id()
    )
    return redirect(url_for('show_all_ships'))


@app.route('/ship/<int:ship_id>/edit', methods=['GET'])
@requires_login
def edit_ship(ship_id):
    ship = get_ship_by_id(ship_id)

    if not ship:
        flash("This ship doesn't exist")
        return redirect(url_for('show_all_ships'))
    if ship.captain_id != current_user.get_id(): 
        flash('You do not own this ship')
        return redirect(url_for('show_all_ships'))
    if ship.departure_time < datetime.datetime.now():
        flash('This ship already left')
        return redirect(url_for('show_all_ships'))

    return render_template(
        "edit_ship.html",
        ship=ship,
        form=EditShip(request.form),
        )


@app.route('/ship/<int:ship_id>/edit', methods=['POST'])
@requires_login
def edit_ship_post(ship_id):
    edit_ship_form = EditShip(request.form)
    ship = get_ship_by_id(ship_id)

    if not ship:
        flash("This ship doesn't exist")
        return redirect(url_for('show_all_ships'))
    if ship.captain_id != current_user.get_id(): 
        flash('You do not own this ship')
        return redirect(url_for('show_all_ships'))
    if ship.departure_time < datetime.datetime.now():
        flash('This ship already left')
        return redirect(url_for('show_all_ships'))

    intended_departure = edit_ship_form.departure_time.data
    current_date = datetime.date.today()
    to_compare = datetime.datetime.combine(current_date, intended_departure)

    if to_compare < datetime.datetime.now():
        flash('The time you have entered has already passed')
        return redirect(url_for('show_all_ships'))

    destination = edit_ship_form.destination.data
    edit_ship_by_id(ship.id, to_compare, destination)

    flash('Your ship has been updated!')
    return redirect(url_for('show_all_ships'))


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

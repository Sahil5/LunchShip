import datetime
from app import app
from flask import flash, redirect, url_for, request, render_template, jsonify
from flask.ext.login import current_user, login_user, logout_user
from auth import check_auth, requires_login, User, render_login
from helpers.forms import LoginForm, AddShip, EditShip, JoinShip
from helpers.view import handle_user_form
from logic import create_ship
from logic import join_lunch_ship
from logic import abandon_lunch_ship
from logic import get_all_sailing_ships
from logic import get_ships_captained
from logic import get_ships_crewed
from logic import get_biggest_ships
from logic import get_ship_by_id
from logic import edit_ship_by_id


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
    sailing_ships = get_all_sailing_ships()
    for sailing_ship in sailing_ships:
        for crew_member in sailing_ship.crew:
            if current_user.get_id() == crew_member.sailor_id:
                sailing_ship.is_crew_member = True

    return render_template(
        "all_ships.html",
        sailing_ships=sailing_ships
    )


@app.route('/ships/all/json', methods=['GET'])
def all_ships_json():
    ships = get_all_sailing_ships()
    return jsonify(
        ships=[
            {
                'id': ship.id,
                'captain_id': ship.captain_id,
                'destination': ship.destination,
                'time_created': str(ship.time_created),
                'departure_time': str(ship.departure_time),
                'crew': [c.sailor_id for c in ship.crew],
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


@app.route('/ship/<int:ship_id>/abandon')
@requires_login
def abandon_ship(ship_id):
    flash('You have just abandoned ship %d' % ship_id)
    abandon_lunch_ship(
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


@app.route('/leaderboards')
def show_leaderboard():
    return render_template(
        'leaderboards.html',
        ships_captained=get_ships_captained(),
        ships_crewed=get_ships_crewed(),
        biggest_ships=get_biggest_ships(),
    )


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

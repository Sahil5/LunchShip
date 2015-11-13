import datetime

from app import app
from flask import flash, redirect, url_for, request, render_template, session
from flask.ext.login import current_user, login_user, logout_user
from auth import check_auth, requires_login, User
from helpers.forms import CreateLunchShip, LoginForm

from logic import create_ship
from presentation.ships import get_all_lunch_ship_presenters

@app.route("/")
@requires_login
def index():
    return redirect(url_for('show_all_ships'))


@app.route('/new_ship', methods=['GET', 'POST'])
@requires_login
def create_new_ship():
    lunch_ship_form = CreateLunchShip(request.form)

    if request.method == 'POST' and lunch_ship_form.validate():
        create_ship(
            session["username"],
            lunch_ship_form.destination.data,
            datetime.datetime.combine(
                datetime.date.today(),
                lunch_ship_form.departure_time.data,
            ),
            lunch_ship_form.crew.data,
        )

        return redirect(url_for('show_all_ships'))

    return render_template(
        "home.html",
        lunch_ship_form=lunch_ship_form
    )


@app.route('/all_ships')
@requires_login
def show_all_ships():
    lunch_ship_presenters = get_all_lunch_ship_presenters()

    # TODO: Add logic for deciding on which projects a person is captain of
    is_captain = True

    return render_template("all_ships.html",
        lunch_ship_presenters=lunch_ship_presenters,
        is_captain=is_captain

    )

@app.route('/join_ship')
@requires_login
def join_ship():
    ## TODO: add logic for joining ship
    flash('You have just joined a new ship')

    return redirect(url_for('show_all_ships'))

@app.route('/edit_ship')
@requires_login
def edit_ship():
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

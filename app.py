import jinja2
from flask import Flask, session, flash, redirect, url_for, request, get_flashed_messages, jsonify, render_template
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user
from auth import check_auth

import secrets


app = Flask(__name__)
app.secret_key = secrets.SECRET_KEY


login_manager = LoginManager()
login_manager.init_app(app)


class UserNotFoundError(Exception):
    pass


# model for user sessions
class User(UserMixin):
    def __init__(self, username):
        self.id = username


# Flask-Login use this to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(username):
    return User(username)


@app.route("/")
def index():
    if current_user.is_authenticated:
        username = current_user.get_id()
        return render_template(
            "home.html",
            msg="hello {}".format(username),
        )

    return redirect(url_for('login'))


@app.route('/login')
def login():
    messages = ', '.join([str(msg) for msg in get_flashed_messages()])
    return '''
        <p>{}</p>
        <form method="post">
            <p>Username: <input name="username" type="text"></p>
            <p>Password: <input name="password" type="password"></p>
            <input type="submit">
        </form>
    '''.format(messages)

@app.route('/login', methods=['post'])
def login_check():
    username = request.form['username']
    password = request.form['password']
    if check_auth(username, password):
        login_user(User(username))
    else:
        flash('Username or password incorrect')

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

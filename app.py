from flask import Flask, session
from auth import requires_auth
import secrets


app = Flask(__name__)
app.debug = True
app.secret_key = secrets.SECRET_KEY


@app.route("/")
@requires_auth
def hello():
    return "Hello {}!".format(session['username'])


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

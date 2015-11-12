import jinja2

from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route("/")
def display_homepage():

    return render_template(
        "home.html",
        msg="hello world"
    )


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

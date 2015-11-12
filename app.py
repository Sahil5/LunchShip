import jinja2

from flask import Flask, request
from flask import render_template

from helpers.forms import CreateLunchShip


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def display_homepage():
    lunch_ship_form = CreateLunchShip(request.form)
    if request.method == 'POST' and lunch_ship_form.validate():
        pass

    return render_template(
        "home.html",
        lunch_ship_form=lunch_ship_form
    )

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

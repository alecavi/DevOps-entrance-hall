from dotenv import dotenv_values
from flask import Flask, render_template, session, redirect, url_for, request
import requests

config = dotenv_values(".env")

app = Flask(__name__)
app.debug = True
app.secret_key = config["SECRET_KEY"]


@app.route("/")
def root():
    if not session.get("logged_in", False):
        return redirect(url_for("login"))
    # TODO: redirect user to their content page


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        response = requests.post(
            url=config["USER_DB"] + "/user/register",
            json={"name": username, "password": password},
        )
        if response.status_code == 200:
            session["logged_in"] = True
            error = None
            # TODO: redirect user to their content page
        elif response.status_code == 409:
            error = "The username \"{}\" is already taken".format(username)
        elif response.status_code == 422:
            if not username:
                error = "Username can't be empty"
            elif len(password) < 8:
                error = "Password must be at least 8 characters"
        return render_template("register.html", error=error, username=username, password=password)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        response = requests.post(
            url=config["USER_DB"] + "/user/check_login",
            json={"name": username, "password": password},
        )
        if response.status_code == 200:
            session["logged_in"] = True
            error = None
            # TODO: redirect user to their content page
        elif response.status_code == 401:
            error = "Username and password don't match"
        elif response.status_code == 404:
            error = "No user \"{}\" exists".format(username)
        elif response.status_code == 422:
            if not username:
                error = "Username can't be empty"
            elif len(password) < 8:
                error = "Password must be at least 8 characters"

        return render_template("login.html", error=error, username=username, password=password)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

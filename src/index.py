from dotenv import dotenv_values
from flask import Flask, render_template, session, redirect, url_for, request
import requests

config = dotenv_values(".env")
USER_DB = config["USER_DB"] + "/user"
VIDEO_INDEX = config["VIDEO_INDEX"] + "/myflix/videos"

app = Flask(__name__)
app.debug = True
app.secret_key = config["SECRET_KEY"]


@app.route("/")
def root():
    if session.get("username") is None:
        return redirect(url_for("login"))
    return redirect(url_for("video"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        response = requests.post(
            url=USER_DB + "/register",
            json={"name": username, "password": password},
        )
        if response.status_code == 200:
            session["username"] = username
            return redirect(url_for("video"))
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
            url=USER_DB + "/check_login",
            json={"name": username, "password": password},
        )
        if response.status_code == 200:
            session["username"] = username
            session["user_id"] = response.json()["id"]
            return redirect(url_for("video"))
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


@app.route("/video")
def video():
    username = session.get("username")
    if username is None:
        return redirect(url_for("login"))

    # Random recommended video:
    recommended_video = requests.get(
        config["VIDEO_INDEX"] + "/myflix/videos/_aggrs/sample-one"
    ).json()[0]

    # request liked and watch later
    response = requests.get(
        config["USER_DB"] + "/user/{}".format(session["user_id"])
    ).json()
    likes = response["likes"]
    watch_later = response["watch_later"]

    # List of liked videos:
    requests.get(
        config
    )

    return render_template(
        "video.html",
        username=username, ip=video["ip"], file=video["file"],
        pic=video["pic"], title=video["Name"], category=video["category"]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

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
        VIDEO_INDEX + "/_aggrs/sample-one"
    ).json()[0]

    # request liked and watch later
    response = requests.get(
        USER_DB + "/{}".format(session["user_id"])
    ).json()
    likes = response["likes"]
    watch_later = response["watch_later"]

    # List of liked videos:
    liked_videos = requests.get(
        VIDEO_INDEX + '?filter={{"uuid": {{"$in": {} }}'.format(likes)
    ).json()

    return render_template(
        "video.html",
        username=username,
        recommended_video=recommended_video,
        liked_videos=liked_videos  # TODO: update template to use this
    )


@app.route("/api/like", methods=["POST"])
def like():
    data = request.json()
    update = "add" if data["state"] else "remove"
    requests.put(
        USER_DB + "{}/like{}".format(session["user_id"], data["video_id"]),
        json='{{"update": {}}}'.format(update)
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

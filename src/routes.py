from dotenv import dotenv_values
from flask import Flask, render_template, session, redirect, url_for, request
import requests

from config import VIDEO_INDEX, USER_DB, SECRET_KEY

app = Flask(__name__)
app.debug = True
app.secret_key = SECRET_KEY


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

    # request liked and watch later
    response = requests.get(
        USER_DB + "/{}".format(session["user_id"])
    ).json()
    likes = set(response["likes"])
    watch_later = set(response["watch_later"])

    # Random recommended video:
    recommended_video = requests.get(
        VIDEO_INDEX + "/_aggrs/sample-one"
    ).json()[0]
    uuid = recommended_video["uuid"]
    recommended = {
        "video": recommended_video,
        "like": uuid in likes,
        "watch_later": uuid in watch_later,
    }

    # liked videos:
    liked = requests.get(
        VIDEO_INDEX + '?filter={"uuid": {"$in": {}}}'.format(list(likes))
    ).json()
    liked = map(
        lambda video: {
            "video": video,
            "like": video["uuid"] in likes,
            "watch_later": video["uuid"] in watch_later,
        },
        liked
    )

    return render_template(
        "video.html",
        username=username,
        recommended=recommended,
        liked=liked
    )


@app.route("/api/like", methods=["POST"])
def like():
    json = request.json
    update = "add" if json["state"] else "remove"
    requests.put(
        USER_DB + "/{}/like/{}".format(session["user_id"], json["video_id"]),
        json={"update": update}
    )
    return ('', 204)


@app.route("/api/watch-later", methods=["POST"])
def watch_later():
    json = request.json
    update = "add" if json["state"] else "remove"
    requests.put(
        USER_DB +
        "/{}/watch-later/{}".format(session["user_id"], json["video_id"]),
        json={"update": update}
    )
    return ('', 204)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

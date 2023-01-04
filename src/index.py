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


@app.route("/test")
def test():
    response = requests.post("http://example.org")
    app.logger.warning("status: %s, url: %s",
                       response.status_code, response.url)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        path = "http://35.217.29.110/user/register/"
        app.logger.warning("PATH: %s", path)
        response = requests.post(
            url=path,
            json={"name": username, "password": password},
            headers={'Content-type': 'application/json',
                     'Accept': 'text/plain'}
        )
        if response.status_code == 200:
            session["logged_in"] = True
        else:
            app.logger.warning(
                "STATUS_CODE: %s, URL: %s",
                response.status_code, response.url
            )

    return render_template("login.html", error=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

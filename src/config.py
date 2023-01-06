from dotenv import dotenv_values


config = dotenv_values(".env")
SECRET_KEY = config["SECRET_KEY"]
USER_DB = config["USER_DB"] + "/user"
VIDEO_INDEX = config["VIDEO_INDEX"] + "/myflix/videos"

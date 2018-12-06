import time, os

from flask import Flask, jsonify, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/home")
def index():
    twatts = db.execute("SELECT * FROM twatts").fetchall()
    return render_template("home.html",twatts=twatts)

@app.route("/post-twatt")
def post():
    #when I login, I have a certain user id. How do I pass that value into the twatts table?
    twatt=request.form.get("twatt")
    db.execute("INSERT INTO twatts (twatt) VALUES (:twatt)",{"twatt":twatt})
    db.commit()

@app.route("/profile", methods=["POST"])
def posts():

    # Get start and end point for posts to generate.
    # start = int(request.form.get("start") or 0)
    # end = int(request.form.get("end") or (start + 9))

    # Generate list of posts.
    data = []
    for i in range(start, end + 1):
        data.append(f"Post #{i}")

    # Artificially delay speed of response.
    time.sleep(1)

    # Return list of posts.
    return jsonify(data)
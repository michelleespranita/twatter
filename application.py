import time, os

from flask import Flask, jsonify, render_template, request
from sqlalchemy import create_engine # sqlalchemy is used to connect Python and SQL
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/registerring",methods=["POST"])
def registerring():
    firstname=request.form.get("firstname")
    lastname=request.form.get("lastname")
    name = firstname + ' ' + lastname
    email=request.form.get("email")
    username=request.form.get("username")
    password=request.form.get("password")
    bio=request.form.get("bio")
    # Check if username and email are still available
    if db.execute("SELECT * FROM userInfo WHERE username=:username",{"username": username}).rowcount==0 and db.execute("SELECT * FROM userInfo WHERE email=:email",{"email": email}).rowcount==0:
        db.execute("INSERT INTO userInfo (name,email,username,password,bio) VALUES (:name,:email,:username,:password,:bio)",{"name":name, "email":email, "username":username, "password":password, "bio":bio})
        db.commit()
        return render_template("success.html")
    else:
        return render_template("errorUNtaken.html")

@app.route("/home", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        twatt = request.form.get("twatt")
        if twatt:
            db.execute("INSERT INTO twatts (twatt) VALUES (:twatt)",{"twatt":twatt})
            db.commit()
    twatts = db.execute("SELECT * FROM twatts").fetchall()
    return render_template("home.html",twatts=twatts)


# @app.route("/profile", methods=["POST"])
# def posts():

#     # Get start and end point for posts to generate.
#     # start = int(request.form.get("start") or 0)
#     # end = int(request.form.get("end") or (start + 9))

#     # Generate list of posts.
#     data = []
#     for i in range(start, end + 1):
#         data.append(f"Post #{i}")

#     # Artificially delay speed of response.
#     time.sleep(1)

#     # Return list of posts.
#     return jsonify(data)

if __name__ == '__main__':
    app.run()
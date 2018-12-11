import time, os

from flask import Flask, jsonify, render_template, request, session, redirect, url_for, escape, g, make_response # make_response allows me not only to return HTML, but to return whatever I want
from flask_session import Session
from sqlalchemy import create_engine # sqlalchemy is used to connect Python and SQL
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = "uuu"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# CREATE TABLE twatts (
#   id SERIAL PRIMARY KEY,
#   username_id INTEGER REFERENCES userInfo(id),
#   twatt VARCHAR NOT NULL
# );

# class Twatt (db.Model):
#     __tablename__ = 'twatts'
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(320))
#     created_time = db.Column(db.DateTime)
#     retwatts = db.Column(db.Integer)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     user = db.relationship('User', back_populates='twatts') # adds a ".twatts" attribute to class User

# # CREATE TABLE userInfo (
# #   id SERIAL PRIMARY KEY,
# #   name VARCHAR NOT NULL,
# #   email VARCHAR UNIQUE,
# #   username VARCHAR UNIQUE,
# #   password VARCHAR NOT NULL,
# #   bio VARCHAR DEFAULT '',
# #   nofollowers INTEGER DEFAULT 0,
# #   nofollowing INTEGER DEFAULT 0,
# #   noTwatt INTEGER DEFAULT 0
# # );

# class User (db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(200), unique=True)
#     username = db.Column(db.String(20), unique=True)
#     password = db.Column(db.String(50), nullable=False)
#     created = db.Column(db.DateTime)
#     bio = db.Column(db.String(200))
#     location = db.Column(db.String(50))
#     statuses = db.Column(db.Integer, default=0)
#     followers = db.Column(db.Integer, default=0)
#     following = db.Column(db.Integer, default=0)
#     twatts = db.relationship('Tweet', back_populates='user') # adds a ".user" attribute to class Tweet

# db.create_all()

@app.before_request # executed before the route '/'
def before_request():
    g.user=None
    if 'user' in session:
        g.user=session['user']

@app.route("/", methods=['GET','POST'])
def index():
    if request.method=='POST':
        session.pop('user', None)
        username=request.form.get("usernamelogin")
        password=request.form.get("passwordlogin")
        # is this correct?
        get_userID=db.execute("SELECT * FROM userInfo WHERE username=:username AND password=:password",{"username": username, "password": password}).fetchone()
        userID=get_userID['id']
        if userID:
            session['user']=username
            response = redirect(url_for("home",username=username))
            response.set_cookie('YourSessionCookie', str(userID)) # assigns the value userID to YourSessionCookie # set_cookie only receives string values, so we must first convert userID from int to string!
            return response
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
    return render_template("errorUNtaken.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    userID = request.cookies.get('YourSessionCookie') # userID is a string
    if userID:
        if g.user:
            username_id = int(userID) # userID must be converted to an integer
            twatt = request.form.get("twatt")
            if twatt:
                db.execute("INSERT INTO twatts (username_id,twatt) VALUES (:username_id,:twatt)",{"username_id":username_id,"twatt":twatt})
                db.commit()
            twatts = db.execute("SELECT username,twatt FROM twatts JOIN userInfo ON userInfo.id = twatts.username_id").fetchall()
            get_bio = db.execute("SELECT * FROM userInfo WHERE id=:id",{"id":username_id}).fetchone() # doesn't work with fetchall()
            bio=get_bio['bio']
            statistics = db.execute("SELECT notwatt,followers,following FROM userInfo WHERE id=:id",{"id":username_id}).fetchall() # returns the number of twatts, followers and following
            return render_template("home.html",username=g.user,twatts=twatts,bio=bio,statistics=statistics)
    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session.pop('Username', None)
    return redirect(url_for('index'))


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
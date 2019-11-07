from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Entry, Emotion, EntryEmotion, Character, EntryCharacter, Theme, EntryTheme, Setting, EntrySetting, connect_to_db, db


app = Flask(__name__)

app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

"""registeration for site"""

@ app.route("/register", methods=['GET'])
def registration_form():

    username = request.args.get("username")
    email = request.args.get("email")
    password = request.args.get("password")
    fname = request.args.get("fname")
    lname = request.args.get("fname")
    gender = request.args.get("gender")
    age = request.args.get("age")

    return render_template("register_form.html",
                            username = username,
                            email=email,
                            password=password,
                            fname=fname,
                            lname=lname,
                            gender=gender,
                            age=age)

@app.route("/register", methods=['POST'])
def registration_process():

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    gender = request.form["gender"]

    if User.query.filter(User.email == email).first():
        #checks if user is already registered by checking if email in database
        return redirect("/")
        #or to login page?

    else:
        #create new user in database
        user = User(username = username,
                    email=email,
                    password=password,
                    fname=fname,
                    lname=lname,
                    gender=gender,
                    age=age)
        db.session.add(user)
        db.session.commit()

    return redirect("/")

"""login to website"""

@app.route("/login", methods=['GET'])
def login_form():

    username = request.args.get("username")
    password = request.args.get("password")
    return render_template("login_form.html",
                            email=email,
                            password=password)

@app.route("/login", methods=['POST'])
def handle_login():

    email = request.form['email']
    password = request.form['password']

    q = User.query.filter(User.email == email, User.password == password).first()


    if q:
        
        session['curent user_id'] = q.user_id
        flash("Logged in")
    
    return redirect("/")










if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')



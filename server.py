from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

# from flask_debugtoolbar import DebugToolbarExtension

from model import User, Entry, Emotion, EntryEmotion, Character, EntryCharacter, Theme, EntryTheme, Setting, EntrySetting, connect_to_db, db


app = Flask(__name__)

app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined

#flask login

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
    age = request.form["age"]

    if User.query.filter(User.email == email).first():
        #checks if user is already registered by checking if email in database
        flash("you have an account already")
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
        flash("successfully registered")


    return redirect("/")

"""login to website"""

@app.route("/login", methods=['GET'])
def login_form():

    username = request.args.get("username")
    password = request.args.get("password")
    return render_template("login_form.html",
                            username=username,
                            password=password)

@app.route("/login", methods=['POST'])
def handle_login():

    username = request.form["username"]
    password = request.form['password']

    q = User.query.filter(User.username == username, User.password == password).first()


    if q:
        session['current_user_id'] = q.user_id
        flash("Logged in")
        #work on flash
        return redirect("/journal")

    else:
        flash("Log in Failed")
        return redirect("/")

"""log out of website"""
@app.route('/logout')
def logout():
    session.pop('current_user_id', None)
    flash("you were logged out")
    return redirect('/')

"""index page, shows past week of posts (title, date, ratings), (drafts), and calendar, (eventually other peoples dreams"""
@app.route('/index')
def show_index():
    return render_template("/index.html")



"""journal page w all entries (with every detail).. profile style, eventually infinite scroll"""
@app.route("/journal", methods=['GET'])
def show_journal():

    logged_user = session['current_user_id']
    


    entries = Entry.query.filter(Entry.user_id == logged_user).all()


    # get session object of user with user user_id
  

    # then relationship it with entries like User.entries

    # then loop over entries in journal.html with jinja to show all entries! 
     
    return render_template("journal.html",
                            entries=entries)



@app.route("/entryform", methods=['GET'])
def show_entryform():

    if 'current_user_id' not in session:
        return redirect("/login")

    else:
        date = request.args.get("date")
        text_content = request.args.get("text_content")
        title = request.args.get("title")
        hours_slept = request.args.get("hours_slept")
        mood_awake = request.args.get("mood_awake")
        mood_sleep = request.args.get("mood_sleep")
        lucidity = request.args.get("lucidity")
        lucid_intent = request.args.get("lucid_intent")

        return render_template("entryform.html",
                                date=date,
                                text_content=text_content,
                                title=title,
                                hours_slept=hours_slept,
                                mood_awake=mood_awake,
                                mood_sleep=mood_sleep,
                                lucidity=lucidity,
                                lucid_intent=lucid_intent)

@app.route("/entryform", methods=['POST'])
def process_entryform():

    date = request.form["date"]
    text_content = request.form["text_content"]
    title = request.form["title"]
    hours_slept = request.form["hours_slept"]
    mood_awake = request.form["mood_awake"]
    mood_sleep = request.form["mood_sleep"]
    lucidity = request.form["lucidity"]
    lucid_intent = request.form["lucid_intent"]
    user_id = session['current_user_id']

    entry = Entry(user_id=user_id,
                  date=date,
                  text_content=text_content,
                  title=title,
                  hours_slept=hours_slept,
                  mood_awake=mood_awake,
                  mood_sleep=mood_sleep,
                  lucidity=lucidity,
                  lucid_intent=lucid_intent)
    
    db.session.add(entry)
    db.session.commit()
    flash("successfully saved entry")

    #create its own entry details page
    return redirect("/entry_details/<entry_id>")


"""edit entry"""


@app.route('/entry_details/<entry_id>', methods=['GET'])
def show_entry_details(entry_id):
    """show individual entry"""

   
    entry = Entry.query.filter(Entry.entry_id == entry_id).first()

    return render_template("entry_details.html",
                            entry_id=entry_id,
                            entry=entry)















if __name__ == "__main__":

    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')



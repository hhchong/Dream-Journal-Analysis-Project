from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

# from flask_debugtoolbar import DebugToolbarExtension

from model import User, Entry, Emotion, EntryEmotion, Character, EntryCharacter, Theme, EntryTheme, Setting, EntrySetting, connect_to_db, db

from peewee import *

from playhouse.sqlite_ext import *


app = Flask(__name__)

app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined

#FIGURE OUT flask login

@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@ app.route("/register", methods=['GET'])
def registration_form():
    """show registration form for site"""

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
    """process registration form"""

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

"""FIGURE OUT how to keep someone logged in so it doesnt redirect to homepage but to index"""
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
    logged_user = session['current_user_id']
    entries = Entry.query.filter(Entry.user_id == logged_user).order_by(Entry.date.desc()).all()
    return render_template("/index.html",
                            entries=entries)



"""journal page w all entries (with every detail).. profile style, eventually infinite scroll"""
@app.route("/journal", methods=['GET'])
def show_journal():

    logged_user = session['current_user_id']
    


    entries = Entry.query.filter(Entry.user_id == logged_user).order_by(Entry.date.desc()).all()


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
        clarity = request.args.get("clarity")
        lucidity = request.args.get("lucidity")
        lucid_intent = request.args.get("lucid_intent")
        emotions = request.args.get("emotions")
        characters = request.args.get("characters")
        themes = request.args.get("themes")
        settings = request.args.get("settings")


        return render_template("entryform.html",
                                date=date,
                                text_content=text_content,
                                title=title,
                                hours_slept=hours_slept,
                                mood_awake=mood_awake,
                                clarity=clarity,
                                lucidity=lucidity,
                                lucid_intent=lucid_intent,
                                emotions=emotions,
                                characters=characters,
                                themes=themes,
                                settings=settings)

@app.route("/entryform", methods=['POST'])
def process_entryform():

    date = request.form["date"]
    text_content = request.form["text_content"]
    title = request.form["title"]
    hours_slept = request.form["hours_slept"]
    mood_awake = request.form["mood_awake"]
    clarity = request.form["clarity"]
    lucidity = request.form["lucidity"]
    lucid_intent = request.form["lucid_intent"]
    user_id = session['current_user_id']
    emotions = request.form.getlist("emotions")
    characters = request.form.getlist("characters")
    themes = request.form.getlist("themes")
    settings = request.form.getlist("settings")


    entry = Entry(user_id=user_id,
                  date=date,
                  text_content=text_content,
                  title=title,
                  hours_slept=hours_slept,
                  mood_awake=mood_awake,
                  clarity=clarity,
                  lucidity=lucidity,
                  lucid_intent=lucid_intent)
    db.session.add(entry)
    db.session.commit()
    
    for emotion in emotions:

        query_emotion = Emotion.query.filter(Emotion.emotion_id == emotion).first()
        
        print(query_emotion)
            
        emotion = EntryEmotion(entry_id=entry.entry_id, emotion_id=query_emotion.emotion_id)

        db.session.add(emotion)
        db.session.commit()

    for character in characters:

        query_character = Character.query.filter(Character.character_id == character).first()

        character = EntryCharacter(entry_id=entry.entry_id, character_id=query_character.character_id)

        db.session.add(character)
        db.session.commit()

    for theme in themes:

        query_theme = Theme.query.filter(Theme.theme_id == theme).first()

        theme = EntryTheme(entry_id=entry.entry_id, theme_id=query_theme.theme_id)

        db.session.add(theme)
        db.session.commit()

    for setting in settings:

        query_setting = Setting.query.filter(Setting.setting_id == setting).first()

        setting = EntrySetting(entry_id=entry.entry_id, setting_id=query_setting.setting_id)

        db.session.add(setting)
        db.session.commit()



    flash("successfully saved entry")

    #create its own entry details page
    return redirect("/index")


"""edit entry"""






@app.route('/entry_details/<entry_id>', methods=['GET'])
def show_entry_details(entry_id):
    """show individual entry"""

   
    entry = Entry.query.filter(Entry.entry_id == entry_id).first()

    return render_template("entry_details.html",
                            entry_id=entry_id,
                            entry=entry)




# """search entries using word"""
# @app.route('/search', methods=['GET'])
# def search():
#     search_query = request.args.get('searchthis')

#     query = Entry.search(search_query)

#     if search_query:
#         query = Entry.search(search_query)
#     else:
#         query = Entry.public().order_by(Entry.timestamp.desc())

#     return object_list('search.html', query, search=search_query, query=query,check_bounds=False )



#ilike query to search through text content

#JSONIFY STUFF....FOR CHARTS
@app.route('/charts')
def show_charts():
    """Show charts"""

    user_id = session['current_user_id']

    return render_template('charts.html')




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



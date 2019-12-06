from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)

# from flask_debugtoolbar import DebugToolbarExtension

from model import User, Reminder, Entry, Emotion, EntryEmotion, Character, EntryCharacter, Theme, EntryTheme, Setting, EntrySetting, connect_to_db, db

from peewee import *

from collections import Counter

from playhouse.sqlite_ext import *

from twilio.rest import Client
# from flask_sqlalchemy import SQLAlchemy

import os
import schedule
import time


from datetime import datetime, timedelta

from sqlalchemy import and_


app = Flask(__name__)

app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined

# ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
# AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
# TWILIO_NUMBER = os.environ['TWILIO_NUMBER']

# #FIGURE OUT flask login
# def morning_text(user):
#     return f"Good morning { user }. Remember to journal your dream!"
# def send_text():
#     client = Client(ACCOUNT_SID, AUTH_TOKEN)
  
#     user= User.query.get(1)
#     reminder = Reminder.query.filter(Reminder.user_id == 1).first()

#     text=morning_text(user.fname)

#     phone=user.phone
#     message = client.messages.create(body=text, from_=TWILIO_NUMBER, to=phone)
#     print(TWILIO_NUMBER)
#     print(phone)
#     return('success')

# schedule.every().day.at("17:53").do(send_text)
  


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html", logged=False)


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

@app.route("/login", methods=['GET'])
def login_form():

    username = request.args.get("username")
    password = request.args.get("password")
    return render_template("login_form.html",
                            username=username,
                            password=password,
                            logged=False)

@app.route("/login", methods=['POST'])
def handle_login():

    username = request.form["username"]
    password = request.form['password']

    q = User.query.filter(User.username == username, User.password == password).first()


    if q:
        session['current_user_id'] = q.user_id
        flash("Logged in")
        #work on flash
        return redirect("/index")

    else:
        flash("Log in Failed")
        return redirect("/")

"""log out of website"""
@app.route('/logout')
def logout():
    session.pop('current_user_id', None)
    flash("you were logged out")
    return redirect('/')

"""index page, shows past week of posts (title, date, ratings), (drafts), and calendar, and reminders"""
@app.route('/index')
def show_index():
    logged_user = session['current_user_id']
    entries = Entry.query.filter(Entry.user_id == logged_user).order_by(Entry.date.desc()).all()
    reminders = Reminder.query.filter(Reminder.user_id == logged_user).order_by(Reminder.day_start.desc()).all()

    return render_template("/index.html",
                            entries=entries,
                            reminders=reminders,
                            logged=True)

@app.route('/stats')
def get_stats():
    """get stats for stat cards in index"""

    user_id = session['current_user_id']
    user = User.query.get(user_id)
    
    thirty_days_ago = datetime.today() - timedelta(days = 30)
    one_week_ago = datetime.today() - timedelta(days = 7)
    previous_week = one_week_ago - timedelta(days = 7)

    lucid_month = Entry.query.filter(Entry.user_id == user.user_id, Entry.date >= thirty_days_ago, Entry.lucidity >= 3).all()
    week_sleep = Entry.query.filter(Entry.user_id == user.user_id, Entry.date >= one_week_ago).all()
    prev_week_sleep = Entry.query.filter(Entry.user_id == user.user_id, Entry.date < one_week_ago, Entry.date >= previous_week).all()

    total_entries = 0
    sleep_percent = 0
    total_lucid_month = 0
    total = 0
    prev_total = 0
    lucid_percent = 0

    for entry in user.entries:
        total_entries += 1

    for lucid in lucid_month:
        total_lucid_month += 1

    for sleep in week_sleep:
        total += sleep.hours_slept
        average_sleep = total/len(week_sleep)
    
    for s in prev_week_sleep:
        prev_total += s.hours_slept
        prev_average_sleep = prev_total/len(prev_week_sleep)

    if average_sleep > prev_average_sleep:
        percent = str((average_sleep - prev_average_sleep)*100)
        change = "UP " + percent + "% from last week"

    elif average_sleep == prev_average_sleep:
        change = "Same average sleep as last week"
    else:
        percent = str((prev_average_sleep - average_sleep)*100)
        change = "DOWN " + percent + "% from last week"

    return jsonify({"total_entries" : total_entries,
                    "total_lucid_month" : total_lucid_month,
                    "average_sleep" : average_sleep,
                    "change" : change})

@app.route('/getPostTitle/<post_id>')
def get_post_by_id(post_id):
    """get the new title that'll show up when updated"""

    search_entry = Entry.query.get(post_id)

    data = {'title' : search_entry.title}

    return jsonify(data)



"""journal page w all entries (with every detail).. profile style, eventually infinite scroll"""
@app.route("/journal", methods=['GET'])
def show_journal():

    logged_user = session['current_user_id']
    user = User.query.filter(User.user_id == logged_user).first()


    entries = Entry.query.filter(Entry.user_id == logged_user).order_by(Entry.date.desc()).all()

     
    return render_template("journal.html",
                            entries=entries,
                            user=user,
                            logged=True)

@app.route("/reminderform", methods=['GET'])
def show_reminderform():
    """show reminder form"""
    day_start = request.args.get("day_start")
    reminder_type = request.args.get("reminder_type")
    additional_info = request.args.get("additional_info")

    return render_template("reminderform.html",
                            day_start=day_start,
                            reminder_type=reminder_type,
                            additional_info=additional_info,
                            logged=True)

@app.route("/reminderform", methods=['POST'])
def process_reminderform():
    """process form and save to db"""
    day_start = request.form["day_start"]
    reminder_type = request.form["reminder_type"]
    additional_info = request.form["additional_info"]
    user_id = session['current_user_id']

    reminder = Reminder(day_start=day_start,
                        reminder_type=reminder_type,
                        additional_info=additional_info,
                        user_id=user_id)

    db.session.add(reminder)
    db.session.commit()

    flash("successfully saved reminder")
    return redirect("/index")

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
                                settings=settings,
                                logged=True)

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
        
        # print(query_emotion)
            
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



@app.route('/entry_details/<entry_id>', methods=['GET'])
def show_entry_details(entry_id):
    """show individual entry"""

   
    entry = Entry.query.filter(Entry.entry_id == entry_id).first()

    return render_template("entry_details.html",
                            entry_id=entry_id,
                            entry=entry,
                            logged=True)

@app.route('/search', methods=['GET'])
def search_term():
    """search through text_content with phrase"""

    user_id = session['current_user_id']
    # user = User.query.get(user_id)

    phrase = request.args.get('search')
  
    if phrase:
         entries = Entry.query.filter(Entry.user_id == user_id, Entry.text_content.ilike(f'%{phrase}%')).all()
    else:
         entries = Entry.query.filter(Entry.user_id == user_id).order_by(Entry.date.desc()).all()

    return render_template('search.html', entries=entries, logged=True)

@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    """delete entry from database"""

    entry_id = request.form.get('entry_id')

    entry = Entry.query.get(entry_id)

    entry.emotions.clear()
    entry.characters.clear()
    entry.themes.clear()
    entry.settings.clear()

    db.session.delete(entry)
    db.session.commit()

    return jsonify({'status' : 'deleted'})

@app.route('/populate_modal', methods=['POST'])
def populate_modal():
    """populate edit modal with original entry info"""
    #figure out how to add tags to this.... checkboxes

    entry_id = request.form.get('entry_id')

    entry = Entry.query.get(entry_id)

    populate_modal_dict= {'title' : entry.title,
                            'text' : entry.text_content}

    return json.dumps(populate_modal_dict)


@app.route('/edit_entry', methods=['POST'])
def edit_entry():
    """edit text entry and save to database"""

    entry_id = request.form.get('entry_id')

    entry = Entry.query.get(entry_id)

    new_title = request.form["title"]
    new_text = request.form["text"]

    entry.title = new_title
    entry.text_content = new_text

    db.session.commit()
    return jsonify({'status' : 'yay'})


@app.route('/lucid.json')
def show_lucidity():
    """render lucid tag on calendar"""

    user_id = session['current_user_id']
    user = User.query.get(user_id)

    # user = User.query.get(1)

    dates = []
    lucidity = []
    lucid = {}
    lucid_data = []

    for entry in user.entries:
        if int(entry.lucidity) >= 3:
            lucidity.append('lucid')
            date = str(entry.date)[:10]
            dates.append(date)
            

    for i in range(0, len(dates)):
        lucid['title'] = lucidity[i]
        lucid['start'] = dates[i]
        lucid['sort'] = '1'
        

        lucid_data.append(lucid.copy())
    print(lucid_data)

    return jsonify(lucid_data)

@app.route('/calendar.json')
def show_calendar_entries():
    """render entries on calendar"""

    user_id = session['current_user_id']
    user = User.query.get(user_id)
    # user = User.query.get(1)


    dates = []
    titles = []
    links = []
    # lucids = []
    event = {}
    events = []

    for entry in user.entries:
        date = str(entry.date)[:10]
        dates.append(date)
        title = str(entry.title)
        titles.append(title)
        link = "/entry_details/" + str(entry.entry_id) 
        links.append(link)

        # if int(entry.lucidity) >= 3:
        #     lucids.append('')


        
    for i in range(0, len(dates)):
         event['title'] = titles[i]
         event['start'] = dates[i]
         event['url'] = links[i]
         event['sort'] = '-1'
         #if 
         events.append(event.copy())
    
    return jsonify(events)

#JSONIFY STUFF....FOR CHARTS
@app.route('/charts')
def show_charts():
    """Show page with charts"""

    user_id = session['current_user_id']

    return render_template('charts.html', logged=True)


@app.route('/emotions_data.json')
def return_emotions():
    """return how often each emotion occurs in all dreams"""

    user_id = session['current_user_id']
    user = User.query.get(user_id)

    emotions = []
    emotions_dict = {}

    for entry in user.entries:
        for emotion in entry.emotions:
            #increment value by one each time an emotion appears in a dream entry
            emotions_dict[emotion.emotion] = emotions_dict.get(emotion.emotion, 0) + 1


    # for emotion in emotions:
    #     emotions_dict[emotion] = emotions_dict.get(emotion, 0) + 1

    chart_emotion_dict = {'labels' : list(emotions_dict.keys()), 
                        'datasets': [{
                        'data': list(emotions_dict.values()), 
                        'backgroundColor': ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#7180AC", "#2B4570", '#A8D0DB', '#E49273']}]}
    # for emotion in emotions_dict.keys():
    #     emotion_str = str(emotion)
    #     emotion_name = emotion_str[30:-1]
    #     chart_emotion_dict['labels'].append(emotion_name)

    # val = list(emotions_dict.values())

    # chart_emotion_dict['datasets'][0]['data'].append(val)

    return jsonify(chart_emotion_dict)

@app.route('/characters_data.json')
def return_characters():
    """return how often characters occur in all dreams"""
    user_id = session['current_user_id']
    user = User.query.get(user_id)

    characters = []
    characters_dict = {}

    for entry in user.entries:
        for character in entry.characters:
            #increment value by one each time a character appears in a dream entry
            characters_dict[character.character] = characters_dict.get(character.character, 0) + 1

    chart_character_dict = {'labels' : list(characters_dict.keys()), 
                        'datasets': [{
                        'data': list(characters_dict.values()), 
                        'backgroundColor': ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#7180AC", "#2B4570", '#A8D0DB', '#E49273', '#98afd4']}]}

    return jsonify(chart_character_dict)


@app.route('/themes_data.json')
def return_themes():
    """return how often themes occur in all dreams"""

    user_id = session['current_user_id']
    user = User.query.get(user_id)

    themes = []
    themes_dict = {}

    for entry in user.entries:
        for theme in entry.themes:
            #increment value by one each time a theme appears in a dream entry
            themes_dict[theme.theme] = themes_dict.get(theme.theme, 0) + 1

    chart_theme_dict = {'labels' : list(themes_dict.keys()), 
                        'datasets': [{
                        'data': list(themes_dict.values()), 
                        'backgroundColor': ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#7180AC", "#2B4570", '#A8D0DB', '#E49273','#98afd4']}]}

    return jsonify(chart_theme_dict)

@app.route('/settings_data.json')
def return_settings():
    """return how often settings occur in all dreams"""
    user_id = session['current_user_id']
    user = User.query.get(user_id)

    settings = []
    settings_dict = {}

    for entry in user.entries:
        for setting in entry.settings:
            #increment value by one each time a setting appears in a dream entry
            settings_dict[setting.setting] = settings_dict.get(setting.setting, 0) + 1

    chart_setting_dict = {'labels' : list(settings_dict.keys()), 
                        'datasets': [{
                        'data': list(settings_dict.values()), 
                        'backgroundColor': ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850","#7180AC", "#2B4570", '#A8D0DB', '#E49273']}]}

    return jsonify(chart_setting_dict)

@app.route('/lucidity_data.json')
def return_lucidity():
    """return lucid progress over all dreams"""
    user_id = session['current_user_id']
    user = User.query.get(user_id)

    date_lst = []
    lucidity_lst = []
    lucid_intent_lst = []
    clarity_lst = []

    for entry in user.entries:
        date = entry.date.strftime('%m/%d/%Y') 
        date_lst.append(date)
        lucidity_lst.append(entry.lucidity)
        lucid_intent_lst.append(entry.lucid_intent)
        clarity_lst.append(entry.clarity)

    chart_lucidity_dict = {'labels' : date_lst,
                            'datasets' : [{
                            'data' : lucidity_lst,
                            'label' : "Lucidity",
                            'borderColor': "#41C3C0",
                            'fill': True,
                            'backgroundColor': "rgba(145, 221, 220, .5)"
                            },
                            {'data' : lucid_intent_lst,
                            'label' : "Lucid Intent",
                            'borderColor': "##8e5ea2",
                            'fill': True
                            },
                            {
                            'data' : clarity_lst,
                            'label' : "Clarity",
                            'borderColor': "#3cba9f",
                            'fill': True
                            }
                            ]}

    return jsonify(chart_lucidity_dict)

@app.route('/sleepquality_data.json')
def return_sleepquality():
    """hours slept for all dreams in the past week for the gradient chart"""
    user_id = session['current_user_id']
    user = User.query.get(user_id)

    hours_lst = []
    date_lst = []

    for entry in user.entries:
        date = entry.date.strftime('%m/%d/%Y')
        date_lst.append(date)
        hours_lst.append(entry.hours_slept)

    chart_hours_dict = {'labels' : date_lst,
                            'datasets' : [{
                            'data' : hours_lst,
                            'label' : "Hours Slept",
                            'borderColor': "#41C3C0",
                            'fill': True,
                            'backgroundColor': "rgba(145, 221, 220, .5)"
                            }
                            ]}

    return jsonify(chart_hours_dict)

# mood chart as line (gradient line no fill) mixed with emotions as positive/negative??? as bars. 

@app.route('/mood_data.json')
def return_mood():
    """mood and positive/negative dream emotions"""
    user_id = session['current_user_id']
    user = User.query.get(user_id)

    postive = 0
    negative = 0
    positive_dict = {}
    negative_dict = {}
    mood_lst = []
    date_lst = []

    for entry in user.entries:
        date = entry.date.strftime('%m/%d/%Y')
        date_lst.append(date)
        mood = entry.mood_awake - 3
        mood_lst.append(mood)
        positive_dict[date] = 0
        negative_dict[date] = 0
        for item in entry.emotions:
            emotion = str(item)
            if "happy" in emotion or "peaceful" in emotion:
                positive_dict[date] = positive_dict.get(date, 0) + 1
            elif "angry" in emotion or "stressed" in emotion or "confused" in emotion or "worried" in emotion or "guilty" in emotion or "sad" in emotion: 
                negative_dict[date] = negative_dict.get(date, 0) - 1
            elif "surprised" in emotion:
                pass
                

    chart_mood_dict = {'labels': date_lst,
                        'datasets' : [{
                            'type' : 'line',
                            'data' : mood_lst,
                            'label' : 'Mood',
                            'fill' : False,
                            'borderColor': "#41C3C0",
                            'yAxisID' : 'left-axis'
                        },
                            {

                            'data' : list(positive_dict.values()),
                            'label' : 'positive',
                            'fill' : True,
                            # 'type': "bar",
                            'borderColor': "#3cba9f",
                            'backgroundColor' : "#3cba9f",
                            'yAxisID' : 'right-axis'

                        },
                            {
                            'data' : list(negative_dict.values()),
                            'label' : 'negative',
                            'fill' : True,
                            'borderColor': "#e8c3b9",
                            'backgroundColor' : "#e8c3b9",
                            'yAxisID' : 'right-axis'
                            }
                        ]}


    return jsonify(chart_mood_dict)







if __name__ == "__main__":

    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    connect_to_db(app)
    app.debug = True
    # while True:
    #     schedule.run_pending() 
    #     time.sleep(1)
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    # connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')



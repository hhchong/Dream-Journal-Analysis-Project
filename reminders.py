from twilio.rest import Client
import os
import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
import schedule
from datetime import date, timedelta
import time
from server import app
from model import *

ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_NUMBER = os.environ['TWILIO_NUMBER']

def morning_text(user):
    return f"Good morning { user }. Remember to journal your dream!"
def send_text():
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
  
    user= User.query.get(1)
    reminder = Reminder.query.filter(Reminder.user_id == 1, Reminder.reminder_type == "Periodic Reality Checks").first()
    time = str(reminder.day_start)[11:16]


    text=morning_text(user.fname)
    phone=user.phone
    message = client.messages.create(body=text, from_=TWILIO_NUMBER, to=phone)
    print("message sent")
    return time 

    

schedule.every().day.at("18:00").do(send_text)
# schedule.every(10).seconds.do(send_text)

 


if __name__ == "__main__":

    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    connect_to_db(app)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

 
    app.debug = True
    # while True:
    #     schedule.run_pending() 
    #     time.sleep(1)
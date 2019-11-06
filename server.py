from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
# from flask_debugtoolbar import DebugToolbarExtension

from model import User, Entry, Emotion, entryEmotion, Character, entryCharacter, Theme, entryTheme, Setting, entrySetting, Lucid, entryLucid, Mood, entryMood, connect_to_db, db


app = Flask(__name__)
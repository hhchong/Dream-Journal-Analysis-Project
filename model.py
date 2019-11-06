""" Models and database functions for dreams project."""



from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#############################################################
# Model definitions

#figure out db.session add/commit, adding data

class User(db.Model):
    """User of dreams website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100))
    username = db.Column(db.String(20))
    password = db.Column(db.String(64))
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    age = db.Column(db.Integer)

    def __repr__(self):
        """ Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} email={self.email} username={self.username} password={self.password} fname={self.fname} lname={self.lname} gender={self.gender} age={self.age}>"


class Entry(db.Model):
    """Entry of dreams website."""

    __tablename__ = "entries"

    entry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, 
                                db.ForeignKey('users.user_id'))
    date = db.Column(db.DateTime)
    text_content = db.Column(db.String(5000))
    title = db.Column(db.String(80))
    hours_slept = db.Column(db.Integer)

    #relationship to tags w manytomany association tables
    emotions = db.relationship("Emotion",
                                secondary="entries_emotions",
                                backref="entries")
    characters = db.relationship("Character",
                                secondary="entries_characters",
                                backref="entries")
    themes = db.relationship("Theme",
                                secondary="entries_themes",
                                backref="entries")

    settings = db.relationship("Setting",
                                secondary="entries_settings",
                                backref="entries")

    lucid = db.relationship("Lucid",
                                secondary="entries_lucid",
                                backref="entries")

    moods = db.relationship("Mood",
                                secondary="entries_moods",
                                backref="entries")

    #Define relationship to user
    user = db.relationship("User")


    def __repr__(self):

        return f"<Entry entry_id={self.entry_id} user_id={self.user_id} date={self.date} text_content={self.text_content} title={self.title} hourse_slept={self.hours_slept}>"


class Emotion(db.Model):
    """Emotions of entry."""

    __tablename__ = "emotions"

    emotion_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    emotion = db.Column(db.String(64))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Emotion emotion_id={self.emotion_id} emotion={self.emotion}>"


class entryEmotion(db.Model):
    """many-to-many association table for emotions and entries"""

    __tablename__ = 'entries_emotions'

    ent_emo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.entry_id'))
    emotion_id = db.Column(db.Integer, db.ForeignKey('emotions.emotion_id'))

    #Define reltionships to entries table and emotions table

    def __repr__(self):

        return f"<Entries Emotion ent_emo_id={self.ent_emo_id} entry_id={self.entry_id} emotion_id={self.emotion_id}>"


class Character(db.Model):
    """Characters of entry"""

    __tablename__ = "characters"

    character_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    character = db.Column(db.String(64))

    def __repr__(self):

        return f"<Character character_id={self.character_id} character={self.character}>"


class entryCharacter(db.Model):
    """many-to-many association table for characters and entries"""

    __tablename__ = 'entries_characters'

    ent_char_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.entry_id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.character_id'))

    def __repr__(self):

        return f"<Entries Character ent_char_id={self.ent_char_id} entry_id={self.entry_id} character_id={self.character_id}>"


class Theme(db.Model):
    """Themes of entry"""

    __tablename__ = "themes"

    theme_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    theme = db.Column(db.String(64))

    def __repr__(self):

        return f"<Theme theme_id={self.theme_id} theme={self.theme}>"

class entryTheme(db.Model):
    """many-to-many association table for characters and entries"""

    __tablename__ = "entries_themes"

    ent_theme_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.entry_id'))
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.theme_id'))

    def __repr__(self):

        return f"<Entries Theme ent_theme_id={self.theme_id} entry_id={self.entry_id} theme_id={self.theme_id}>"


class Setting(db.Model):
    """Settings of entry"""

    __tablename__ = "settings"

    setting_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    setting = db.Column(db.String(64))

    def __repr__(self):

        return f"<Setting setting_id={self.setting_id} setting={self.setting}>"


class entrySetting(db.Model):
    """many-to-many association table for settings and entries"""

    __tablename__ = "entries_settings"

    ent_set_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.entry_id'))
    setting_id = db.Column(db.Integer, db.ForeignKey('settings.setting_id'))

    def __repr__(self):

        return f"<Entries Setting ent_set_id={self.ent_set_id} entry_id={self.entry_id} setting_id={self.setting_id}>"


class Lucid(db.Model):
    """Lucid states of entry"""

    __tablename__ = "lucid"

    lucid_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    lucid_state = db.Column(db.Integer)
    lucid_intent = db.Column(db.Integer)

    def __repr__(self):

        return f"<Lucid lucid_id={self.lucid_id} lucidity={self.lucid_state} lucid_intent={self.lucid_intent}>"


class entryLucid(db.Model):
    """many-to-many association table for lucid states and entries"""

    __tablename__ = "entries_lucid"

    ent_lucid_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.entry_id'))
    lucid_id = db.Column(db.Integer, db.ForeignKey('lucid.lucid_id'))

    def __repr__(self):

        return f"<Entries Lucid ent_lucid_id={self.ent_lucid_id} entry_id={self.entry_id} lucid_id={self.lucid_id}>"


class Mood(db.Model):
    """Overall moods of entry awake/asleep"""

    __tablename__ = "moods"

    mood_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    mood_awake = db.Column(db.Integer)
    mood_asleep = db.Column(db.Integer)

    def __repr__(self):

        return f"<Mood mood_id={self.mood_id} mood_awake={self.mood_awake} mood_asleep={self.mood_asleep}>"


class entryMood(db.Model):
    """many-to-many association table for moods and entries"""

    __tablename__ = "entries_moods"

    ent_mood_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.entry_id'))
    mood_id = db.Column(db.Integer, db.ForeignKey('moods.mood_id'))

    def __repr__(self):

        return f"<Entries Moods ent_mood_id={self.ent_mood_id} entry_id={self.entry_id} mood_id={self.mood_id}>"

#####################################################################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dreams'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")






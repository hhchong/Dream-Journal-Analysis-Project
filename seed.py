"""File to seed tags for categories in entries."""

from sqlalchemy import func
from model import Emotion, Character, Theme, Setting, Intensity
"""from model import the different tag categories"""

from model import connect_to_db, db
from server import app


emotions_tags=["angry", "stressed", "confused", "happy", "peaceful", "surprised", "worried", "guilty", "sad"]
characters_tags=["friend", "significant_other", "animal", "parent", "child", "celebrity", "relative", "stranger", "ex", "non_human"]
themes_tags=["fun", "dramatic", "violent", "sexuality", "relationships", "nightmare", "spiritual", "friendly", "action", "loss"]
settings_tags=["outdoor", "indoor", "school", "home", "work", "automobile", "familiar", "unfamiliar"]
intensity_tags=[ 1, 2, 3, 4, 5]


def load_emotions():
    """load emotions into database."""
    print("Emotions")

    Emotion.query.delete()

    for tag in emotions_tags:
        emotion_index = emotions_tags.index(tag) + 1
        add_emotion = Emotion(emotion_id= emotion_index, emotion=tag)

        db.session.add(add_emotion)

    db.session.commit()



def load_characters():
    """load characters into database."""
    print("Characters")

    Character.query.delete()

    for tag in characters_tags:
        character_index = characters_tags.index(tag) + 1
        add_character = Character(character_id=character_index, character=tag)

        db.session.add(add_character)

    db.session.commit()


def load_themes():
    """load themes into database."""
    print("Themes")

    Theme.query.delete()

    for tag in themes_tags:
        theme_index = themes_tags.index(tag) + 1
        add_theme = Theme(theme_id=theme_index, theme = tag)

        db.session.add(add_theme)

    db.session.commit()


def load_settings():
    """load settings into database."""
    print("Settings")

    Setting.query.delete()

    for tag in settings_tags:
        setting_index = settings_tags.index(tag) + 1
        add_setting = Setting(setting_id=setting_index, setting=tag)

        db.session.add(add_setting)

    db.session.commit()
    

def load_intensity():
    """load intensity into database."""
    print("Intensity")

    Intensity.query.delete()

    for level in intensity_tags:
        intensity_index = intensity_tags.index(level) + 1
        add_intensity = Intensity(intensity_id=intensity_index, intensity=level)

        db.session.add(add_intensity)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_emotions()
    load_characters()
    load_themes()
    load_settings()
    load_intensity()






from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    playerName = StringField('Player Name')
    submit = SubmitField('Search')
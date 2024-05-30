from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    playerName = StringField('Player Name')
    submit = SubmitField('Search')

class CompareForm(FlaskForm):
    playerName1 = StringField('First Player')
    playerName2 = StringField('Second Player')
    submit = SubmitField('Compare')
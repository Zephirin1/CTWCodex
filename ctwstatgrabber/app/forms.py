from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    playerName = StringField('Player Name', validators=[DataRequired()])
    submit = SubmitField('Search')

class CompareForm(FlaskForm):
    playerName1 = StringField('First Player', validators=[DataRequired()])
    playerName2 = StringField('Second Player', validators=[DataRequired()])
    submit = SubmitField('Compare')
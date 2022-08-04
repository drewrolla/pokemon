from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class PokeSearchForm(FlaskForm):
    poke_name = StringField('Pokemon Name', validators=[InputRequired()])
    submit = SubmitField()


# not required to have 5 pokemon to make a team, just need one
class PokeTeam(FlaskForm): 
    pokemon1 = StringField('Pokémon', validators=[InputRequired()])
    pokemon2 =  StringField('Pokémon', validators=[])
    pokemon3 = StringField('Pokémon', validators=[])
    pokemon4 = StringField('Pokémon', validators=[])
    pokemon5 = StringField('Pokémon', validators=[])
    submit = SubmitField()
    
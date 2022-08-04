import requests
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from .forms import PokeTeam, PokeSearchForm
from app.models import User, Team, db

poke = Blueprint('poke', __name__, template_folder='poketemplates')

@poke.route('/pokemon', methods=["GET", "POST"])
def getPokemon():
    form = PokeSearchForm()
    my_dict = {}
    if request.method == "POST":
        print('Post request made.')
        if form.validate():
            poke_name = form.poke_name.data
            url = f"https://pokeapi.co/api/v2/pokemon/{poke_name}"
            res = requests.get(url)
            if res.ok:
                data = res.json()
                my_dict = {
                    'name': data['name'],
                    'ability': data['abilities'][0]['ability']['name'],
                    'img_url': data['sprites']['front_shiny'],
                    "hp": data['stats'][0]['base_stat'],
                    'attack': data['stats'][1]['base_stat'],
                    'defense': data['stats'][2]['base_stat']
                }
    return render_template('pokemon.html', form=form, pokemon=my_dict)

# create pokemon teams stuff
@poke.route('/team/create', methods=["GET", "POST"])
@login_required # checks to see if user is logged in - if so, they can use function, if not, too bad :P
def createTeam():
    form = PokeTeam()
    if request.method == "POST":
        if form.validate():
            pokemon1 = form.pokemon1.data
            pokemon2 = form.pokemon2.data
            pokemon3 = form.pokemon3.data
            pokemon4 = form.pokemon4.data
            pokemon5 = form.pokemon5.data

            team = Team(pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, current_user.id)

            db.session.add(team)
            db.session.commit()


    return render_template('createteam.html', form=form)

# show all teams
@poke.route('/allteams', methods=["GET", "POST"])
def showAllTeams():
    team = Team.query.all()
    return render_template('allteams.html', team=team)


# show your team (kind of the same as the above, might just combine so it's less redundant/confusing)
@poke.route('/team', methods=["GET", "POST"])
def showTeamPage():
    team = Team.query.all()
    return render_template('myteam.html', team=team)


# shows one team in particular
@poke.route('/team/<int:team_id>', methods=["GET", "POST"])
def showMyTeam(team_id):
    team = Team.query.get(team_id)
    # can also do like this: team = Team.query.filter_by(id=team_id).first()
    return render_template('singleteam.html', team=team)


# edit team
@poke.route('/team/edit/<int:team_id>', methods=["GET", "POST"])
def editTeam(team_id):
    form = PokeTeam()
    team = Team.query.get(team_id)
    if current_user.id != team.user_id:
        return redirect(url_for('poke.showMyTeam'), team_id=team_id)
    if request.method=="POST":
        if form.validate():
            pokemon1 = form.pokemon1.data
            pokemon2 = form.pokemon2.data
            pokemon3 = form.pokemon3.data
            pokemon4 = form.pokemon4.data
            pokemon5 = form.pokemon5.data

            team.pokemon1 = pokemon1
            team.pokemon2 = pokemon2
            team.pokemon3 = pokemon3
            team.pokemon4 = pokemon4
            team.pokemon5 = pokemon5

            db.session.commit()
            return redirect(url_for('poke.showMyTeam'), team_id=team_id)

    return render_template('editteam.html', form=form, team=team)


# deletes team
@poke.route('/team/delete', methods=["GET", "POST"])
def deleteTeam():
    return render_template('createteam.html')
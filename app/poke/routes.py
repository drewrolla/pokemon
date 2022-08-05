import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .forms import PokeTeam, PokeSearchForm
from app.models import Pokemon, User, Team, db

poke = Blueprint('poke', __name__, template_folder='poketemplates')

@poke.route('/pokemon', methods=["GET", "POST"])
def getPokemon():
    form = PokeSearchForm()
    my_dict = {}
    is_caught = False
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
                    'hp': data['stats'][0]['base_stat'],
                    'attack': data['stats'][1]['base_stat'],
                    'defense': data['stats'][2]['base_stat']
                }
                pokemon = Pokemon.query.filter_by(name=my_dict['name']).first()
                if not pokemon:
                    pokemon = Pokemon(my_dict['name'], my_dict['ability'], my_dict['img_url'], my_dict['hp'], my_dict['attack'], my_dict['defense'])
                    pokemon.save()
                if current_user.team.filter_by(name=pokemon.name).first():
                    is_caught = True
    return render_template('pokemon.html', form=form, pokemon=my_dict, is_caught=is_caught)

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
            team.save()
            flash('Team saved!', 'success')
        else:
            flash('Invalid input. Please try again.', 'danger')

    return render_template('createteam.html', form=form)

# show all teams
@poke.route('/allteams', methods=["GET", "POST"])
def showAllTeams():
    team = Team.query.order_by(Team.date_created.desc()).all()
    return render_template('allteams.html', team=team)


# show your team (kind of the same as the above, might just combine so it's less redundant/confusing)
@poke.route('/team', methods=["GET", "POST"])
def showTeamPage():
    team = current_user.team.all()
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
        flash('Action invalid.', 'danger')
        return redirect(url_for('poke.showMyTeam'), team_id=team_id)
    if request.method=="POST":
        if form.validate():
            pokemon1 = form.pokemon1.data
            pokemon2 = form.pokemon2.data
            pokemon3 = form.pokemon3.data
            pokemon4 = form.pokemon4.data
            pokemon5 = form.pokemon5.data

            team.updateTeam(pokemon1, pokemon2, pokemon3, pokemon4, pokemon5)
            team.saveUpdates()
            flash('Team updated!', 'success')
            return redirect(url_for('poke.showTeamPage'))
        else:
            flash('Error updating team. Please try again.', 'danger')

    return render_template('editteam.html', form=form, team=team)


# deletes team
@poke.route('/team/delete/<int:team_id>', methods=["GET", "POST"])
def deleteTeam(team_id):
    team = Team.query.get(team_id)
    if current_user.id != team.user_id:
        flash('Action prohibited.', 'danger')
        return redirect(url_for('poke.showTeamPage'), team_id=team_id)
    team.delete()
    flash('Team deleted.', 'success')
    return render_template('allteams.html')


# catch pokemon
@poke.route('/catch/<string:pokemon_name>')
def catchPokemon(pokemon_name):
    # user
    current_user
    # pokemon
    pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
    if len(current_user.team.all()) < 5:
        current_user.team.append(pokemon)
        db.session.commit()
    else:
        flash('Your team is already full!', 'danger')
    # assume catch function works
    return redirect(url_for('poke.getPokemon'))

# release pokemon
@poke.route('/release/<string:pokemon_name>')
def releasePokemon(pokemon_name):
    pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
    current_user.team.remove(pokemon)
    db.session.commit()
    return redirect(url_for('poke.getPokemon'))

# battle pokemon
@poke.route('/battle')
def battlePage():
    gym = User.query.all()
    return render_template('battle.html', gym=gym)

@poke.route('/battle/<int:user_id>')
def battle(user_id):
    user = User.query.get(user_id)
    team = user.team.all()
    current_user.fightUser(user)
    return render_template('startbattle.html', user=user, team=team)

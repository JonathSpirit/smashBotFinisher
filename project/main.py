from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db, characters

main = Blueprint('main', __name__)


def retrieveNextCharacterToBeKilled():
    next_character = None

    for index_id in range(0, len(characters)):
        if not str(index_id) in current_user.characters:
            next_character = characters[index_id]
            break
        elif not current_user.characters[str(index_id)]["killed"]:
            next_character = characters[index_id]
            break
    return next_character


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    next_character = retrieveNextCharacterToBeKilled()

    return render_template('profile.html',
                           name=current_user.name,
                           charactersData=characters,
                           characters=current_user.characters,
                           nextCharacter=next_character)

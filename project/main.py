from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy.orm.attributes import flag_modified
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from . import db, characters
import os

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


@main.route('/victory', methods=['POST'])
@login_required
def victory():
    victory_image = request.files['fileupload']

    # verify with mimetype if the file is an image .png/.jpg/.jpeg
    if victory_image.mimetype == 'image/png' or victory_image.mimetype == 'image/jpg' or victory_image.mimetype == 'image/jpeg':
        folder_path = "temp/victory/"
        file_path = folder_path + secure_filename(current_user.name + '.' + victory_image.mimetype.split('/')[1])
        os.makedirs(folder_path, exist_ok=True)
        victory_image.save(file_path)
    else:
        flash('File is not an image')

    return redirect(url_for('main.profile'))


@main.route('/defeated', methods=['POST'])
@login_required
def defeated():
    next_character = retrieveNextCharacterToBeKilled()

    if next_character is not None:
        current_death = int(current_user.characters[str(next_character.id)]["death"])
        current_user.characters[str(next_character.id)]["death"] = current_death + 1
        flag_modified(current_user, "characters")
        db.session.add(current_user)
        db.session.commit()

    return redirect(url_for('main.profile'))


@main.route('/profile')
@login_required
def profile():
    next_character = retrieveNextCharacterToBeKilled()

    return render_template('profile.html',
                           name=current_user.name,
                           charactersData=characters,
                           characters=current_user.characters,
                           nextCharacter=next_character)

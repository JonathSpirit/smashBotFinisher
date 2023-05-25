from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy.orm.attributes import flag_modified
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from . import db, characters
import cv2
import pytesseract
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

        victory_image_cv = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)

        # Make sure that the image is in portrait mode
        if victory_image_cv.shape[0] > victory_image_cv.shape[1]:
            victory_image_cv = cv2.rotate(victory_image_cv, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Convert the image to grayscale
        victory_image_preprocess_cv = cv2.cvtColor(victory_image_cv, cv2.COLOR_RGB2GRAY)

        # Apply threshold to get image with only black and white
        victory_image_preprocess_cv = cv2.threshold(victory_image_preprocess_cv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Remove the noise
        victory_image_preprocess_cv = cv2.medianBlur(victory_image_preprocess_cv, 5)

        # Apply dilation or erosion
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
        victory_image_preprocess_cv = cv2.erode(victory_image_preprocess_cv, kernel, iterations=2)

        # Save the preprocessed image
        cv2.imwrite(folder_path+'testCV.png', cv2.cvtColor(victory_image_preprocess_cv, cv2.COLOR_GRAY2BGR))

        # Compute the text from the image
        config = r'-l fra+eng --psm 12 --oem 3'

        text_from_image = pytesseract.image_to_string(victory_image_preprocess_cv, config=config)
        print(text_from_image)

        # Compute the bounding boxes
        boxes = pytesseract.image_to_boxes(victory_image_preprocess_cv, config=config)

        # Draw the bounding boxes
        for b in boxes.splitlines():
            b = b.split(' ')
            victory_image_cv = cv2.rectangle(victory_image_cv, (int(b[1]), victory_image_cv.shape[0] - int(b[2])),
                                             (int(b[3]), victory_image_cv.shape[0] - int(b[4])), (0, 255, 0), 2)

        # Save the image
        cv2.imwrite(folder_path+'testCVBoxes.png', cv2.cvtColor(victory_image_cv, cv2.COLOR_RGB2BGR))
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

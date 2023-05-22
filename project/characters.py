import os
import re


class Characters:

    def __init__(self, character_id, character_name):
        self.id = character_id
        self.name = character_name
        self.profile = 'image/characterSlides/' + str(character_id) + '-' + character_name + '.png'


def characters_init():
    characters = {}

    folder = os.path.dirname(os.path.abspath(__file__)) + '/static/image/characterSlides/'

    # Find all files that being with a number followed by a dash and end with .png with a name between them
    # Example: 1-CharacterName.png

    for filename in os.listdir(folder):
        match = re.search('^(\\d+)-(.+)\\.png$', filename)
        if match:
            character_id = int(match.group(1))
            character_name = str(match.group(2))
            characters[character_id] = Characters(character_id, character_name)
            print(
                'Character ' + str(character_id) + ' ' + character_name + ' added to characters map' + ', profile : ' +
                characters[character_id].profile)
        else:
            print('No match found for ' + filename)

    # Sort the characters dictionary by key
    characters = dict(sorted(characters.items()))
    return characters

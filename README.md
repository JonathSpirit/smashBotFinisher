# Smash bot finisher

## Description
This is a homemade website for a Super Smash Bros Ultimate (SSBU) custom challenge.
The goal is simple, beat every character in the game as level 9 CPU with a single character.

## Copyright
This website is not affiliated with Nintendo or any other company. Images of Smash Bros characters are the property of Nintendo.

This project is an educational project and therefore no official server is provided. If you want to use this website, you will have to host it yourself.

The project is under the MIT license. See the [LICENSE](LICENSE) file for more details.

## Installation
### Requirements
- You will need Python (tested on 3.11)

- Install a virtual environment in the project root (optional but recommended)
```bash
python -m venv venv
```

- Activate the virtual environment (optional but recommended)
```bash
.\venv\Scripts\activate
```

- Install the dependencies
```bash
pip install Flask Flask-Login Flask-SQLAlchemy pyTesseract opencv-python
```

(please follow instructions in the Tesseract-ocr Github page to install it on your system)

- Create the database (in python interpreter)
```bash
python
>>> from project import db, create_app, models
>>> app = create_app()

>>> with app.app_context():
>>>    db.create_all()
```

### Run the server
- Run the server
```bash
python -m flask run
```

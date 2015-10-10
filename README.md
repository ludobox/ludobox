# Ludobox UI

User Interface for Ludobox

## How it works

A python script will generate the following files : a list of all games + a folder containing info of each game.

    python generate.py # generate folders tree

Each game is structured as follow

* ```/games/game/game-info.json```
* ```/games/game/game-files.zip``` # any files attached to the game
* ```/games/game/index.html``` # generated html file

## App structure

* ```games``` : list all games
* ```games/add``` : add new games
* ```games/jeu1``` : display game named "jeu1"

### Data model

Model of a game (JSON)

    {
        "timestamp": "10/10/2015 14:52:35",
        "title": "Borgia, le jeu malsain",
        "description": "Ouais",
        "fab_time": "2+ h",
        "requirements": "IMPRIMANTE",
        "players": 4,
        "duration": "60+",
        "audience": "Adultes",
        "authours": "Michel",
        "illustrators": "Jean-Claude",
        "source": "Le vin",
        "license": "CC 1.0",
        "languages": "Français",
        "themes": "Médiéval, Salopard",
        "type": 0
    }


## Install dependencies

    pip install -r requirements.txt


CSS with [Skeleton](http://getskeleton.com/), 

# Ludobox UI

User Interface for Ludobox

## How it works

A python script will generate the following files : a list of all games + a folder containing info of each game.

    python generate.py # generate folders tree

Each game is structured as follow

    /games/game/game-info.json
    /games/game/game-files.zip # any files attached to the game
    /games/game/index.html # generated html file

## App structure

* ```games``` : list all games
* ```games/add``` : add new games
* ```games/jeu1``` : display game named "jeu1"


## Install dependencies

    pip install -r requirements.txt

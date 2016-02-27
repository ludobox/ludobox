# Ludobox UI

User Interface for the Ludobox project.

## How it works

Install using ```setup.py```

  python setup.py install

A python script ```ludobox``` will generate the following files : a list of all games + a folder containing info of each game.

    ludobox generate # generate folders tree

You can then launch the web server:

    ludobox serve # give http access to ludobox-ui

To know the other usage of the ludocore script:

    ludobox help


### Templating

CSS with [Skeleton](http://getskeleton.com/). Please edit CSS in ```css/style.css```

Each game is structured as follow

* ```/games/game/game-info.json```
* ```/games/game/game-files.zip``` # any files attached to the game
* ```/games/game/index.html``` # generated html file

## App structure

* ```data``` : where the json description and attached files of all games are
* ```data/frululu``` : description and attachement for the game named "frululu"
* ```static``` : all HTML pages are static and served from here
* ```static/bower_components``` : all web dependancies (CSS, JS and fonts) will
  be installed here by bower
* ```static/games``` : list all games
* ```static/games/frululu``` : display game named "frululu"
* ```static/add``` : add new games
* ```static/css``` : project specific CSS
* ```static/js``` : project specific JS
* ```static/images``` : project specific images
* ```templates``` : Jinja2 templates used to generates all the pages
* ```tests``` : location for all the test data used to test the application


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
        "authors": "Michel",
        "illustrators": "Jean-Claude",
        "source": "Le vin",
        "license": "CC 1.0",
        "languages": "Français",
        "themes": "Médiéval, Salopard",
        "type": 0
    }


## Developers

Install ludobox package in development mode

  python setup.py develop # patch path for development env


## Install dependencies  

To install python dependancies:

    pip install -r requirements.txt

To install web dependancies (CSS, JS and fonts):

    bower install

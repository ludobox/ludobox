# Ludobox UI

User Interface for the Ludobox project.

To distribute your games using the Ludobox, see the explanations in [Ludobox Borgia](https://github.com/ludobox/ludobox-borgia).

## Install

Install using ```setup.py```

    python setup.py install

## How it works

A python script ```ludobox``` will generate the following files : a list of all games + a folder containing info of each game.

    ludobox generate # generate folders tree

You can then launch the web server:

    ludobox serve # give http access to ludobox-ui

To know the other usage of the ludocore script:

    ludobox help


## App structure

* ```data``` : where the json description and attached files of all games are
* ```data/frululu``` : description and attachement for the game named "frululu"
* ```static``` : all HTML pages are static and served from here
* ```static/bower_components``` : all web dependancies (CSS, JS and fonts) will
  be installed here by bower
* ```static/games``` : list all games
* ```static/games/frululu``` : a game named "frululu"
* ```static/add``` : add new games
* ```templates``` : Jinja2 templates used to generates all the pages
* ```tests``` : location for all the test data used to test the application
* ```static/customisation``` : directory with all the files that allow customisation of the app (specific Javascript, CSS, images...)

## Developers

Install ludobox package in development mode

    python setup.py develop # patch path for development env

CSS templating using [Skeleton](http://getskeleton.com/). Please edit CSS in ```css/style.css```

## Install dependencies

To install python dependancies:

    pip install -r requirements.txt

To install web dependancies (CSS, JS and fonts):

    bower install

## Using

### App structure

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

### Games

To distribute your games using the Ludobox, see the explanations in [Ludobox Borgia](https://github.com/ludobox/ludobox-borgia).

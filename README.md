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

## Installation

### Install GIT

[TLDR](https://fr.wiktionary.org/wiki/TLDR): If you are under Ubuntu/Debian it's just as simple as:

    sudo apt-get install git

For other platforms or detailed instructions: (GIT download page)[https://git-scm.com/downloads].

### Retrieve the code

In a console go to the directory where you want to retrieve the code and type:

    git clone https://github.com/ludobox/ludobox-ui.git

### Dependencies Installation

#### Python and PIP

[TLDR](https://fr.wiktionary.org/wiki/TLDR): If you are under ubuntu/debian it's just as simple as:

    sudo apt-get install python pip

For any other case here are the detailed instructions...

First you have to install Python: [Python download page](https://www.python.org/downloads/). If you are on Windows you may have python not recognised un the console, the solution is [here](https://stackoverflow.com/questions/6318156/adding-python-path-on-windows-7).

Then you need to install PIP: [How to install PIP](https://pip.pypa.io/en/stable/installing/).

#### Node.js, npm and bower

[TLDR](https://fr.wiktionary.org/wiki/TLDR): If you are under Ubuntu/Debian it's just as simple as:

    sudo apt-get install nodejs npm
    sudo ln -s /usr/bin/nodejs /usr/bin/node # for ubuntu only
    sudo npm install bower -g

For any other case here are the detailed instructions...

First you have to install Node.js and npm (the official installer bring them both): [Node.js download page](https://nodejs.org/en/download/). For windows you can find more details here [Install Node.js and npm on windows](http://blog.teamtreehouse.com/install-node-js-npm-windows).
And finally Bower: [Bower installation guide](https://bower.io/#install-bower).

#### Python dependancies

In console go to in the directory where you have retrieved the ludobox-ui code and install python dependancies:

    python -m pip install -r requirements.txt

#### Web dependancies

In console go to in the directory where you have retrieved the ludobox-ui code and install web dependancies (CSS, JS and fonts):

    bower install

# Licence

    Copyright (C) 2016  Pierre-Yves Martin for DCALK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
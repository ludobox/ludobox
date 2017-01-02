## Installation

Install using ```setup.py```

    python setup.py install

---

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

## Get started

First, let's get our first game [Borgia](https://github.com/ludobox/borgia-le-jeu-malsain) which is our model for the Ludobox system.

    mkdir data # create a data folder to store our game
    cd data
    git clone https://github.com/ludobox/borgia-le-jeu-malsain

A python script ```ludobox``` will generate the following files : a list of all games + a folder containing info of each game.

    ludobox generate # generate folders tree

You can then launch the web server:

    ludobox serve # give http access to ludobox-ui

To know the other usage of the ludocore script:

    ludobox help

## Launching the server

To launch the server type in a console from de ludobox-ui directory:

    python ludocore.py clean
    python ludocore.py generate
    python ludocore.py serve

Hit Ctrl+C in the terminal to terminate the server.

## Installation

### Requirements

You will need `python`, `pip`, `virtualenv` and `git` to install Ludobox (see instructions at the bottom to install these softwares).

### Download the Ludobox code

You can download the code by following this [link](https://github.com/ludobox/ludobox/archive/master.zip)

For [Git](https://git-scm.com/) users, just type in your terminal:

    git clone https://github.com/ludobox/ludobox.git


### Install the program

Navigate to the code folder and type :  

    ./bin/install

That's it !

###  Start your box !

In your terminal :

    ludobox start

In your browser, navigate to [http://localhost:8080](http://localhost:8080)

You can now use your box !


## Dependencies

#### Install GIT

If you are under Ubuntu/Debian it's just as simple as:

    sudo apt-get install git

For other platforms or detailed instructions: (GIT download page)[https://git-scm.com/downloads].

#### Python and PIP

If you are under ubuntu/debian it's just as simple as:

    sudo apt-get install python-pip

#### Virtualenv

We recommend to use a [virtual environment](https://virtualenv.pypa.io/en/stable/) to avoid messing with your system install


    pip install virtualenv
    virtualenv venv
    . venv/bin/activate

You can now safely install Ludobox.

To reset your virtualenv, just delete the folder and create a new one.

    deactivate # exit the virtual env
    rm -R venv # delete the folder

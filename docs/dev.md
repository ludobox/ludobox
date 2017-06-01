## Start developing with Ludobox

Here are all commands to contribute to the development of Ludobox


What we cover here :

1. Install the server app using `./bin/install`
1. Install the client app using `node`
1. Generate some test data
1. Run all tests

### Issues and questions

Issues in questions can be addressed directly on our [Github](https://github.com/ludobox/ludobox/issues)


### Frontend

The client is written in ES6, using `jsx` and React.

We try to follow [Clean Code](https://github.com/ryanmcdermott/clean-code-javascript) standard  

Make sure that you have `node > 4` installed before starting.

    cd client    
    npm install
    npm start

One you got all npm packages correctly, the `npm start` command will watch and rebuild automatically while you develop (using webpack).

#### Testing

    npm test

Get coverage using `npm run coverage`. Results are browsable in HTML at `./client/coverage/`.

#### Build for production

    npm run build

## Server / Backend

The backend is basically a JSON API running on Flask/ Python. Most of the content are static files, except the index.

To install the server, just run `./bin/install`

You can also install directly the Python library using ```setup.py```

    cd server
    python setup.py install

You will need to copy and edit the config file for the app to start

    cp config.yml.sample config.yml

Then you can start the server in debug mode  

    ludobox start --debug

#### Testing

We use py.test to collect and run the tests. There is a wrapper available :

    ludobox test

You can use `ludobox test --trace` to show the complete trace logs.

#### Coverage

If you want to collect information about test coverage, run the following command

    coverage  run --source ludobox -m ludobox test

### Generate (fake) data

For testing purposes, you can generate fake game descriptions using the `faker` app.

    cd bin/faker
    npm install
    npm start



### Documentation

Docs are stored in the `/docs` folder. They are automatically built at [ludobox.readthedocs.io](http://ludobox.readthedocs.io/en/latest/) using [Read the Docs / MkDocs](http://www.mkdocs.org/).


### Release a new version

We use [bumpversion](https://pypi.python.org/pypi/bumpversion) to release new versions of the app. The following sequence will release a patch to github :   

    ./bin/release

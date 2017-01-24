The app is separated in 2 main parts :

* **server** : a JSON api using Python/Flask
* **frontend** : a JS single-page application based on React

All communications between client and server are made through


## Data

All data is stored in `/data`.

### Add some fake data

To test, you need some data. You can generate fake game descriptions using the `faker` app.

    cd bin/faker
    npm install
    npm start

## Server / Backend

### Testing

    py.test tests

### Coverage

    coverage  run --source ludobox -m py.test tests

### Build the docs

  Docs are automatically built on [Read The Docs](http://ludobox.readthedocs.io/en/latest/) using [MkDocs](http://www.mkdocs.org/)

### Release a new version

  pip install bumpversion==0.5.3
  bumpversion patch
  git push origin master --tags


## Client / Frontend

The client is written in ES6, using `jsx`. You need to build it

It tries to follow [Clean Code](https://github.com/ryanmcdermott/clean-code-javascript) standard  

### Dev

Get the deps and watch / rebuild automatically

    cd client    
    npm install
    npm start

### Build

    npm run build

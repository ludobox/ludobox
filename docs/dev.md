### Testing

    ludobox autotest

### Coverage

    coverage  run --source ludobox -m ludobox.main autotest

### Build the docs

  Docs are automatically built on [Read The Docs](http://ludobox.readthedocs.io/en/latest/) using [MkDocs](http://www.mkdocs.org/)

### Release a new version

  pip install bumpversion==0.5.3
  bumpversion patch

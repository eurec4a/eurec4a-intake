# How to contribute

## Adding data-sources

If you would like to add a data source please [fork](https://github.com/eurec4a/eurec4a-intake/fork) this repository,
follow the [intake documentation](https://intake.readthedocs.io/en/latest/catalog.html#remote-access)
to create an entry in [catalog.yml](catalog.yml) (or a separate
yaml-file if you are adding many new data sources) and finally make
a pull-request. Tests are automatically run on pull-requests to ensure
that all defined data sources can be accessed.

Please remember to put an entry into our changelog (`CHANGELOG.md`).

## Write the changelog

We are keeping a changelog in the file `CHANGELOG.md`. Every pull request has to add a summary of what it's doing into that file.
This description is meant as a high level overview of what has been changed, so it should be quick to read and in particular shouldn't be just a verbatim copy of all the commit messages. Another purpose of the changelog is to help with our process of releasing new versions: we'll have to check how severe the changes introduced since the last version are in order to come up with a sensible new version number.

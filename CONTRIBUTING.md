# How to contribute

## Adding data-sources

If you would like to add a data source please [fork](https://github.com/eurec4a/eurec4a-intake/fork) this repository,
follow the [intake documentation](https://intake.readthedocs.io/en/latest/catalog.html#remote-access)
to create an entry in [catalog.yml](catalog.yml).

Please note the general structure of the catalog and its entries:
- Platform specific entries (e.g. `HALO`) and larger products (e.g. `JOANNE`/`C3ONTEXT`) are stored in directories.
- Products containing many data sources shall be added to a separate yaml-file.
- Catalog entries should avoid problematic charaters (e.g. `-`,`+`,`/`) and numbers as first characters to allow catalog access via dot-notation (e.g. cat.BCO.meteorology).
- Problematic characters and numbers may be used in established cases (e.g. cat.HALO.UNIFIED.HAMPradar['HALO-0119'], cat.simulations.botany.nx1536['3D']).

After the catalog entries are complete, please continue with a pull-request to request the addition/change of a datasource. Tests are automatically run on pull-requests to ensure
that all defined data sources can be accessed.

Please remember to put an entry into our changelog (`CHANGELOG.md`).

## Write the changelog

We are keeping a changelog in the file `CHANGELOG.md`. Every pull request has to add a summary of what it's doing into that file.
This description is meant as a high level overview of what has been changed, so it should be quick to read and in particular shouldn't be just a verbatim copy of all the commit messages. Another purpose of the changelog is to help with our process of releasing new versions: we'll have to check how severe the changes introduced since the last version are in order to come up with a sensible new version number.

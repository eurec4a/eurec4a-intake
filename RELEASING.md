# How to make a new release

Making a new release is currently a manual, multi-step process:

1. check that all test are passing (in particular, all data sources are reachable)
2. check the changelog and determine the next version (see below)
3. update the `CHANGELOG.md` such that it states the new version on top and doesn't contain any unreleased entries
4. create a git tag named `vX.Y.Z` according to the new version
5. update the `CHANGELOG.md` such that it contains a new `(unreleased)` placeholder for upcoming changes
6. create the release on github
7. ensure the release is propadated to zenodo

## version number

The version numbers are adapted from the [SEMVER](https://semver.org/) scheme: `MAJOR.MINOR.PATCH`.

In order to decide for the new version number, please check the `CHANGELOG.md`.
Depending on the kind of changes since the last release, it will be a `MAJOR`, `MINOR` or `PATCH` release, according to the following table.
If multiple kinds apply, the highest wins (e.g. on `MINOR` and `MAJOR` changes, it will be a `MAJOR` release).

| change | (minimum) release kind |
|:---:|:---:|:---:|
| add a new endpoint (🔵) | minor |
| delete a previously existing endpoint | major |
| change the content returned by an endpoint (e.g. data version updates) | major |
| change the source location of an endpoint (e.g. from one server to another) | major (❗) |
| moving / renaming an endpoint should be considered as adding and deleting | major |
| changing endpoint metadata (e.g. description) | patch |
| changes to CI | patch |
| changes to requirements.txt (and similar) | patch |

🔵 An endpoint is anything specifying some dataset in intake language, e.g.: `cat["foo"]["bar"](arg="baz")` would be an endpoint. A notable consequence would be, that adding arguments can be minor if the defaults would result in the same dataset being retrieved if the new arguments are not specified by the user.

❗ We've observed that most of the time a dataset is moved, it's actually deleted from the old location. Because of that, the old version would be broken and thus the new version is significantly different.

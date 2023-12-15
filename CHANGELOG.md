# Changelog

## (unreleased)

### New Datasets
* Add isotope data from BCO (#152). By [Hauke Schulz](https://github.com/observingClouds)
* Add EUREC4A-MIP boundary conditions from ERA5 and COSMO for current and pseudo-global warming experiment (#135). By [torresalavez](https://github.com/torresalavez) and [Hauke Schulz](https://github.com/observingClouds)
* Add cloud droplet size distribution from specMACS instrument. By [Veronika Pörtge](https://github.com/vpoertge)
### Updated Datasets
* Updated RV Meteor cloud radar data (LIMRAD94) to version 1.2, in which the variable hydrometeor_mask was added which tells you whether there is a signal in the processed reflectivity or not
### Removed Datasets
### Fixes
### Internal Changes
* update IPFS version in CI to 0.23.0 to improve access times and make weekly_test more reliable (#149). By [Hauke Schulz](https://github.com/observingClouds)
* add citation recommendations (#155). By [Hauke Schulz](https://github.com/observingClouds)

## 1.0.0

### New Datasets
* Stereographically derived cloud geometries from specMACS for all flight legs flown with HALO during the EUREC4A campaign are added, except those where no points could be found, i.e. due to darkness (#142). By [Lea Volkmer](https://github.com/lvol08)
### Updated Datasets
### Removed Datasets
* The previously existing "experimental" dataset has been removed as it was not complete and only for testing reasons (#142). By [Lea Volkmer](https://github.com/lvol08)
### Fixes
### Internal Changes

* add `CONTRIBUTING.md` describing how to contibute
* add `RELEASING.md` describing how to make a new release
* start of changelog

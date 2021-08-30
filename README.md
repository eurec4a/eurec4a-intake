# EUREC4A Intake catalogue

![eurec4a_intake](https://github.com/eurec4a/eurec4a-intake/workflows/eurec4a_intake/badge.svg)

This repository contains an [intake](https://github.com/intake/intake)
catalogue for acessing data from  the [EUREC4A field
campaign](http://eurec4a.eu/) stored on: 1)
[AERIS](https://observations.ipsl.fr/aeris/eurec4a/#/) and 2) Munich
University (via OPeNDAP) and 3) OPeNDAP access to files at
[NOAA's National Center for Environmental Information](https://www.ncei.noaa.gov/thredds-ocean/catalog/psl/atomic/catalog.html) and 4) data linked via [IPFS](https://ipfs.io/).


## Usage

To use you will need to install `intake`, `xarray`, `intake-xarray`,
`zarr`, `pydap`, `requests` and `s3fs`

```bash
pip install intake xarray intake-xarray zarr pydap s3fs requests
```

The catalogue (and underlying data) can then be accessed directly from python:

```python
> from intake import open_catalog
> cat = open_catalog("https://raw.githubusercontent.com/eurec4a/eurec4a-intake/master/catalog.yml")
```

You can list the available sources with:
```python
>> list(cat)
['radiosondes', 'barbados', 'dropsondes', 'halo', 'p3', 'specmacs']

>> list(cat.radiosondes)
['atalante_meteomodem',
 'atalante_vaisala',
 'bco',
 'meteor',
 'ms_merian',
 'ronbrown']
```

Then load up a [dask](https://github.com/dask/dask)-backed `xarray.Dataset` so
that you have access to all the available variables and attributes in the
dataset:

```python
>> ds = cat.radiosondes.ronbrown.to_dask()
>> ds
<xarray.Dataset>
Dimensions:      (alt: 3100, nv: 2, sounding: 329)
Coordinates:
  * alt          (alt) int16 0 10 20 30 40 50 ... 30950 30960 30970 30980 30990
    flight_time  (sounding, alt) datetime64[ns] dask.array<chunksize=(83, 775), meta=np.ndarray>
    lat          (sounding, alt) float32 dask.array<chunksize=(83, 1550), meta=np.ndarray>
    lon          (sounding, alt) float32 dask.array<chunksize=(83, 1550), meta=np.ndarray>
    sounding_id  (sounding) |S1000 dask.array<chunksize=(165,), meta=np.ndarray>
Dimensions without coordinates: nv, sounding
Data variables:
    N_gps        (sounding, alt) float32 dask.array<chunksize=(83, 1550), meta=np.ndarray>
    N_ptu        (sounding, alt) float32 dask.array<chunksize=(83, 1550), meta=np.ndarray>
    alt_bnds     (alt, nv) int16 dask.array<chunksize=(3100, 2), meta=np.ndarray>
...
```

You can then slice and access the data as if you had it available locally

## Adding data-sources

If you would like to add a data source please [fork](https://github.com/eurec4a/eurec4a-intake/fork) this repository,
follow the [intake documentation](https://intake.readthedocs.io/en/latest/catalog.html#remote-access)
to create an entry in [catalog.yml](catalog.yml) (or a separate
yaml-file if you are adding many new data sources) and finally make
a pull-request. Tests are automatically run on pull-requests to ensure
that all defined data sources can be accessed.

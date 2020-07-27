# EUREC4A Intake catalogue (unofficial)

This repository contains an [intake](https://github.com/intake/intake)
catalogue for data from the [EUREC4A field campaign](http://eurec4a.eu/)
accessing data directly from the
[AERIS](https://observations.ipsl.fr/aeris/eurec4a/#/).


## Usage

To use you will need to install `intake` and (currently) a forked
version of [intake-xarray](https://github.com/intake/intake-xarray) from
https://github.com/leifdenby/intake-xarray:

```bash
pip install intake opendap netcdf4
pip install git+https://https://github.com/leifdenby/intake-xarray#egg=intake-xarray
```

You will then need to provide the OPeNDAP authentication information by setting
the `DAP_USER` and `DAP_PASSWORD` environment variables:

```bash
export DAP_USERNAME=<aeris-username>
export DAP_PASSWORD=<aeris-password>
```

The catalogue (and underlying data) can then be accessed directly from python:

```python
> from intake import open_catalogo
> cat = open_catalog("https://raw.githubusercontent.com/leifdenby/eurec4a-intake/catalog.yml")
```

You can list the available sources with:
```python
> list(cat)
['specmacs_cloudmask']
```

Then load up a [dask](https://github.com/dask/dask)-backed `xarray.Dataset` so
that you have access to all the available variables and attributes in the
dataset:
```python
> ds = cat.specmacs_cloudmask.to_dask()
> ds
<xarray.Dataset>
Dimensions:                              (angle: 318, radiation_wavelength: 1, time: 800701)
Coordinates:
  * angle                                (angle) float64 18.0 17.9 ... -17.27
  * time                                 (time) datetime64[ns] 2020-02-18T10:...
  * radiation_wavelength                 (radiation_wavelength) float64 1.601...
Data variables:
    cloud_mask                           (time, angle) uint8 dask.array<chunksize=(800701, 318), meta=np.ndarray>
    brightness_cloud_mask                (time, angle) uint8 dask.array<chunksize=(800701, 318), meta=np.ndarray>
    ...
Attributes:
    title:                           cloud mask derived from specMACS SWIR ca...
    platform_id:                     HALO
    ...
```

You can then slice and access the data as if you had it available locally

# EUREC4A Intake catalogue (unofficial)

![eurec4a_intake](https://github.com/leifdenby/eurec4a-intake/workflows/eurec4a_intake/badge.svg)

This repository contains an [intake](https://github.com/intake/intake)
catalogue for data from the [EUREC4A field campaign](http://eurec4a.eu/)
accessing data from a zarr-backed object-store (using
[minio](https://min.io)) at https://minio.denby.eu.


## Usage

To use you will need to install `intake`, `zarr` and `s3fs`

```bash
pip install intake zarr s3fs
```

The catalogue (and underlying data) can then be accessed directly from python:

```python
> from intake import open_catalog
> cat = open_catalog("https://raw.githubusercontent.com/leifdenby/eurec4a-intake/master/catalog.yml")
```

You can list the available sources with:
```python
>> list(cat)
['radiosondes', 'dropsondes']

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
>> ds = cat.ronbrown.to_dask()
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

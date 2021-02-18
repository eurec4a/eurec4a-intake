# Example on how to read cloud radar data
The high resolution data has about 500 MB per file, which when read in over a remote source can lead to long wait times.
To reduce the wait times the data can be read in using dask.

```python
# open the catalog
> from intake import open_catalog
> cat = open_catalog("https://raw.githubusercontent.com/eurec4a/eurec4a-intake/master/catalog.yml")
```
Select the data you want with the given parameters
to see which parameters are available have a look into the yaml file
```python
> ds = cat.Meteor.cloudradar.high_res(version=1.0)

# to quickly read in the data use read_chunked(), this doesn't load the data into memory yet
> ds1 = ds.read_chunked()
```
Explore the dataset and choose the variable you want to work with.
If you only need a certain variable it's better to only read in this one.
```python
> ds2 = ds1.Zh.compute()
> ds2
<xarray.DataArray 'Zh' (time: 44447, range: 367)>
array([[nan, nan, nan, ..., nan, nan, nan],
       [nan, nan, nan, ..., nan, nan, nan],
       [nan, nan, nan, ..., nan, nan, nan],
       ...,
       [nan, nan, nan, ..., nan, nan, nan],
       [nan, nan, nan, ..., nan, nan, nan],
       [nan, nan, nan, ..., nan, nan, nan]], dtype=float32)
Coordinates:
  * time     (time) datetime64[ns] 2020-02-01T00:00:06.700000047 ... 2020-02-...
  * range    (range) float32 313.0 335.4 357.7 ... 1.288e+04 1.292e+04 1.296e+04
Attributes:
    plot_range:  [-60, 20]
    plot_scale:  linear
    comment:     Calibrated reflectivity. Calibration convention: in the abse...
    long_name:   Radar reflectivity factor
    units:       dBZ
```
The radar reflectivity is now stored in your local memory and you can do further analysis
```python
> import matplotlib.pyplot as plt
> ds2.plot(x='time')  # plot the variable with time as the x axis

```
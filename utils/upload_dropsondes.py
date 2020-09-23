import s3fs
import xarray as xr
import yaml
import os
from pathlib import Path


DATA_ROOT = Path("../dropsondes")

s3_access_key = os.environ['S3_ACCESS_KEY']
s3_secret_key = os.environ['S3_SECRET_KEY']

fs = s3fs.S3FileSystem(
    anon=False,
    key=s3_access_key,
    secret=s3_secret_key,
    client_kwargs={"endpoint_url": "https://minio.denby.eu"},
)

catalogs = dict(
    joanne="EUREC4A_JOANNE_Dropsonde-RD41_Level_3_v0.5.7-alpha%2B0.g45fe69d.dirty.nc",
)

cat_sources = {}


def add_cat_entry(name, description):
    cat_sources[name] = {
        "description": description,
        "driver": "zarr",
        "args": {
            "urlpath": f"simplecache::s3://eurec4a-environment/dropsondes",
            "consolidated": True,
            "storage_options": {
                "s3": {
                    "anon": True,
                    "client_kwargs": {
                        "endpoint_url": "https://minio.denby.eu"
                    }
                }
            }
        }
    }


for cat, fn in catalogs.items():
    print(f"{fn} -> {cat}")
    mapper = fs.get_mapper(f"eurec4a-environment/dropsondes")

    # create xarray dataset somehow, i.e.
    ds = xr.open_dataset(DATA_ROOT/fn)
    desc = f"{ds.attrs['Title']}"
    add_cat_entry(cat, desc)

    # write to object store
    # (if you're connected to a dask distributed cluster, this will run in parallel)
    # (if you pass a regular path instead of `mapper`, you would write to disk instead)
    ds.to_zarr(mapper, consolidated=True)

    # to read back the data after writing, you need to restart your kernel for some reason
    # I think this has to do with s3fs caching
    ds_s3 = xr.open_zarr(mapper, consolidated=True)

catalog = {
    'sources': cat_sources
}

print(yaml.dump(catalog, default_flow_style=False))

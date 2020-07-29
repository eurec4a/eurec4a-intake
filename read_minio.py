import s3fs
import xarray as xr
import os

s3_access_key = os.environ['S3_ACCESS_KEY']
s3_secret_key = os.environ['S3_SECRET_KEY']

fs = s3fs.S3FileSystem(
    anon=False,
    key=s3_access_key,
    secret=s3_secret_key,
    client_kwargs={"endpoint_url": "https://minio.denby.eu"},
)

mapper = fs.get_mapper("eurec4a-environment/radiosondes/bco")

ds_s3 = xr.open_zarr(mapper, consolidated=True)
print(ds_s3)

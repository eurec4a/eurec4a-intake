from pathlib import Path


import intake
import pytest


def get_master_catalog():
    # TODO: replace with environment variable
    p_catalog = Path(__file__).parent.parent/"catalog.yml"
    assert p_catalog.exists()
    return intake.open_catalog(str(p_catalog))


@pytest.fixture
def catalog():
    return get_master_catalog()


ALL_ENTRIES = list(get_master_catalog().walk(depth=10))
@pytest.mark.parametrize("dataset_name", ALL_ENTRIES)
def test_get_intake_source(catalog, dataset_name):
    item = catalog[dataset_name]
    if item.container == "catalog":
        item.reload()
    else:
        item.discover()
        plugin = item.describe()['plugin'][0]
        if plugin in ["opendap", "zarr"]:
            _ = item.to_dask()
        elif plugin in ["intake_esm.esm_datastore", "parquet"]:
            _ = item.get()
        else:
            raise Exception(plugin)

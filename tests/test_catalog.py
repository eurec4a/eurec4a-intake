from intake import open_catalog

CATALOG_URL = "https://raw.githubusercontent.com/leifdenby/eurec4a-intake/master/catalog.yml"

def test_catalog_discover():
    cat = open_catalog(CATALOG_URL)
    cat.discover()

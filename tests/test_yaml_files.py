from pathlib import Path
import yaml
import pytest


def root_path():
    return Path(__file__).parent.parent


def all_catalog_files():
    root = root_path()
    return [str(p.relative_to(root)) for p in sorted(root.glob("**/*.y*ml"))
            if not p.match(".*/**/*")
            and not p.match("tests/**/*")
            and not any(part.startswith(".") for part in p.relative_to(root).parts)]


@pytest.mark.parametrize("filename", all_catalog_files())
def test_no_excess_keys(filename):
    with open(root_path() / filename) as ifp:
        data = yaml.load(ifp, Loader=yaml.SafeLoader)

    excess = set(data) - {"version", "metadata", "user_parameters", "aliases", "data", "entries"}
    assert excess == set()

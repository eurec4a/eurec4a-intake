from pathlib import Path

import intake
import pytest


def root_path():
    return Path(__file__).parent.parent


def get_master_catalog():
    p_catalog = root_path() / "catalog.yml"
    assert p_catalog.exists()
    return intake.open_catalog(str(p_catalog))


@pytest.fixture
def catalog():
    return get_master_catalog()


def _get_catalog_file_from_data(cat, name):
    """Return the source YAML file path for a named entry in a catalog, or None."""
    entry = cat.entries.get(name)
    if entry is None:
        return None
    # The entry kwargs reference a data token like '{data(TOKEN)}'
    args = entry.kwargs.get("args", [])
    for arg in args:
        if isinstance(arg, str) and arg.startswith("{data("):
            tok = arg[len("{data("):-2]
            data_desc = cat.data.get(tok)
            if data_desc is not None:
                url = data_desc.kwargs.get("url", "")
                if url and not url.startswith("http"):
                    return Path(url)
    return None


def all_entries(reference_branch="origin/master"):
    from sh import git

    relevant_files = set(
        l.strip()
        for l in git.log(
            "--oneline",
            "--name-only",
            f"{reference_branch}..HEAD",
            _tty_out=False,
            _iter=True,
        )
    )
    root = root_path()
    relevant_files = set(root / f for f in relevant_files if (root / f).exists())

    def walk_catalog(cat, depth=10):
        if depth == 0:
            return
        for name in cat.entries:
            entry = cat.entries[name]
            if entry.output_instance == "intake.readers.entry:Catalog":
                try:
                    subcat = cat[name].read()
                    yield from walk_catalog(subcat, depth - 1)
                except Exception:
                    pass
            else:
                source_file = _get_catalog_file_from_data(cat, name)
                marks = []
                if source_file is not None and source_file in relevant_files:
                    marks.append(pytest.mark.modified_on_branch)
                yield pytest.param(
                    (cat, name),
                    id=name,
                    marks=marks,
                )

    return list(walk_catalog(get_master_catalog()))


@pytest.mark.parametrize("cat_and_name", all_entries())
def test_get_intake_source(cat_and_name):
    cat, name = cat_and_name
    reader = cat[name]
    output = reader.output_instance
    if output == "xarray:Dataset":
        _ = reader.to_dask()
    elif output in ("builtins:dict",):
        _ = reader.read()
    else:
        raise Exception(f"Unknown output_instance: {output} for entry {name}")


@pytest.mark.modified_on_branch
def test_make_ci_happy_if_no_test_is_selected():
    """pytest returns exit code 5 if no test is selected"""
    pass

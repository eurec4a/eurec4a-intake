"""
Migrate intake v1 YAML catalog files to intake v2 format.

Handles:
  - opendap  -> OpenDAP datatype + XArrayDatasetReader
  - zarr     -> Zarr datatype + XArrayDatasetReader
  - netcdf   -> NetCDF3/HDF5 datatype + XArrayDatasetReader
  - yaml_file_cat / intake.catalog.local.YAMLFileCatalog -> YAMLFile + YAMLCatalogReader
  - json     -> kept as-is (intake 2 has built-in json driver)
  - Removes plugins: block
  - Preserves description, metadata, parameters -> user_parameters
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).parent.parent

XARRAY_READER = "intake.readers.readers:XArrayDatasetReader"
YAML_READER = "intake.readers.readers:YAMLCatalogReader"

OPENDAP_DATATYPE = "intake.readers.datatypes:OpenDAP"
ZARR_DATATYPE = "intake.readers.datatypes:Zarr"
NETCDF_DATATYPE = "intake.readers.datatypes:NetCDF3"
YAML_DATATYPE = "intake.readers.datatypes:YAMLFile"

SIMPLE_UP_CLS = "intake.readers.user_parameters:SimpleUserParameter"

YAML_CAT_DRIVERS = {"yaml_file_cat", "intake.catalog.local.YAMLFileCatalog"}
OPENDAP_DRIVERS = {"opendap"}
ZARR_DRIVERS = {"zarr"}
NETCDF_DRIVERS = {"netcdf"}
JSON_DRIVERS = {"json"}


def _tok(s: str) -> str:
    """Short deterministic hash token matching intake's own scheme."""
    return hashlib.md5(s.encode()).hexdigest()[:16]


def _make_data_entry(datatype: str, kwargs: dict) -> tuple[str, dict]:
    key = _tok(datatype + str(sorted(kwargs.items())))
    entry = {
        "datatype": datatype,
        "kwargs": kwargs,
        "metadata": {},
        "user_parameters": {},
    }
    return key, entry


def _v1_param_to_up(param: dict) -> dict:
    """Convert a v1 parameter dict to a v2 SimpleUserParameter dict."""
    up = {
        "cls": SIMPLE_UP_CLS,
        "dtype": "object",
        "default": str(param.get("default", "")),
        "description": param.get("description", ""),
    }
    return up


def _resolve_catalog_dir(url: str, catalog_dir: Path) -> str:
    """Replace {{CATALOG_DIR}} with the actual catalog directory path."""
    return url.replace("{{CATALOG_DIR}}", str(catalog_dir)).replace("{{ CATALOG_DIR }}", str(catalog_dir))


def _convert_source(name: str, src: dict, catalog_dir: Path | None = None) -> tuple[dict, dict]:
    """
    Convert a single v1 source entry.
    Returns (data_entries_dict, reader_entry_dict).
    data_entries_dict may contain 0 or 1 items (json keeps nothing).
    reader_entry_dict is the entry for the 'entries' section.
    """
    driver = src.get("driver", "")
    args = src.get("args", {}) or {}
    description = src.get("description", "")
    metadata = src.get("metadata", {}) or {}
    parameters = src.get("parameters", {}) or {}

    user_parameters = {
        k: _v1_param_to_up(v) for k, v in parameters.items()
    }

    data_entries = {}

    if driver in OPENDAP_DRIVERS:
        url = _resolve_catalog_dir(args.get("urlpath", ""), catalog_dir) if catalog_dir else args.get("urlpath", "")
        data_kwargs = {"url": url, "options": {}}
        tok, data_entry = _make_data_entry(OPENDAP_DATATYPE, data_kwargs)
        data_entries[tok] = data_entry

        reader_kwargs: dict = {"args": [f"{{data({tok})}}"], "chunks": args.get("chunks", {})}
        if "engine" in args:
            reader_kwargs["engine"] = args["engine"]

        reader_entry = {
            "reader": XARRAY_READER,
            "kwargs": reader_kwargs,
            "output_instance": "xarray:Dataset",
            "user_parameters": user_parameters,
            "metadata": {"description": description, **metadata},
        }

    elif driver in ZARR_DRIVERS:
        url = _resolve_catalog_dir(args.get("urlpath", ""), catalog_dir) if catalog_dir else args.get("urlpath", "")
        consolidated = args.get("consolidated", None)
        data_kwargs: dict = {"url": url, "storage_options": None, "root": ""}
        tok, data_entry = _make_data_entry(ZARR_DATATYPE, data_kwargs)
        data_entries[tok] = data_entry

        reader_kwargs = {"args": [f"{{data({tok})}}"], "chunks": args.get("chunks", {})}
        if consolidated is not None:
            reader_kwargs["consolidated"] = consolidated

        reader_entry = {
            "reader": XARRAY_READER,
            "kwargs": reader_kwargs,
            "output_instance": "xarray:Dataset",
            "user_parameters": user_parameters,
            "metadata": {"description": description, **metadata},
        }

    elif driver in NETCDF_DRIVERS:
        url = _resolve_catalog_dir(args.get("urlpath", ""), catalog_dir) if catalog_dir else args.get("urlpath", "")
        data_kwargs = {"url": url, "storage_options": None}
        tok, data_entry = _make_data_entry(NETCDF_DATATYPE, data_kwargs)
        data_entries[tok] = data_entry

        reader_kwargs = {"args": [f"{{data({tok})}}"], "chunks": args.get("chunks", {})}

        reader_entry = {
            "reader": XARRAY_READER,
            "kwargs": reader_kwargs,
            "output_instance": "xarray:Dataset",
            "user_parameters": user_parameters,
            "metadata": {"description": description, **metadata},
        }

    elif driver in YAML_CAT_DRIVERS:
        path = args.get("path", args.get("urlpath", ""))
        if catalog_dir:
            path = _resolve_catalog_dir(path, catalog_dir)
        data_kwargs = {"url": path, "storage_options": None}
        tok, data_entry = _make_data_entry(YAML_DATATYPE, data_kwargs)
        data_entries[tok] = data_entry

        reader_entry = {
            "reader": YAML_READER,
            "kwargs": {"args": [f"{{data({tok})}}"]},
            "output_instance": "intake.readers.entry:Catalog",
            "user_parameters": user_parameters,
            "metadata": {"description": description, **metadata},
        }

    elif driver in JSON_DRIVERS:
        # Keep json as a passthrough note — intake 2 has no direct json reader
        # that matches v1 semantics; emit a comment-style placeholder entry
        json_url = args.get("urlpath", args.get("path", ""))
        if catalog_dir:
            json_url = _resolve_catalog_dir(json_url, catalog_dir)
        reader_entry = {
            "reader": "intake.readers.readers:JSONReader",
            "kwargs": {"url": json_url},
            "output_instance": "builtins:dict",
            "user_parameters": user_parameters,
            "metadata": {"description": description, **metadata},
        }

    else:
        # Unknown driver — pass through as a best-effort opaque entry
        reader_entry = {
            "reader": f"UNKNOWN:{driver}",
            "kwargs": args,
            "output_instance": "object",
            "user_parameters": user_parameters,
            "metadata": {"description": description, **metadata},
        }

    return data_entries, reader_entry


def migrate_file(path: Path, dry_run: bool = False) -> bool:
    """Migrate a single v1 YAML file to v2 in-place. Returns True if changed."""
    text = path.read_text()
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        print(f"  SKIP (parse error): {e}")
        return False

    if not isinstance(data, dict):
        print("  SKIP (not a dict)")
        return False

    # Already v2?
    if data.get("version") == 2:
        print("  already v2, skipping")
        return False

    sources = data.get("sources", {}) or {}
    top_description = data.get("description", "")

    all_data: dict = {}
    all_entries: dict = {}

    for name, src in sources.items():
        if not isinstance(src, dict):
            continue
        data_entries, reader_entry = _convert_source(name, src, catalog_dir=path.parent)
        all_data.update(data_entries)
        all_entries[name] = reader_entry

    v2 = {
        "version": 2,
        "metadata": {"description": top_description} if top_description else {},
        "user_parameters": {},
        "aliases": {},
        "data": all_data,
        "entries": all_entries,
    }

    out = yaml.dump(v2, default_flow_style=False, allow_unicode=True, sort_keys=False)

    if not dry_run:
        path.write_text(out)
    return True


def all_catalog_files() -> list[Path]:
    files = []
    for p in sorted(ROOT.glob("**/*.y*ml")):
        parts = p.relative_to(ROOT).parts
        if any(part.startswith(".") for part in parts):
            continue
        if parts[0] == "tests":
            continue
        if parts[0] == "utils":
            continue
        files.append(p)
    return files


def main():
    dry_run = "--dry-run" in sys.argv
    targets = [Path(a) for a in sys.argv[1:] if not a.startswith("--")] or all_catalog_files()

    changed = 0
    for p in targets:
        rel = p.relative_to(ROOT)
        print(f"{rel} ...", end=" ")
        if migrate_file(p, dry_run=dry_run):
            print("migrated" if not dry_run else "would migrate")
            changed += 1
        else:
            print()

    print(f"\nDone: {changed}/{len(targets)} files {'would be ' if dry_run else ''}migrated.")


if __name__ == "__main__":
    main()

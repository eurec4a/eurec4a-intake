"""
Pytest configuration and fixtures for the eurec4a-intake test suite.

This module applies workarounds for known incompatibilities between legacy zarr v2
stores and newer versions of xarray / zarr.
"""

import warnings


def _patch_zarr_scalar_dimension_handling():
    """
    Monkey-patch xarray's ZarrStore.open_store_variable to gracefully handle
    zarr v2 scalar arrays that carry incorrect ``_ARRAY_DIMENSIONS`` metadata.

    Some older zarr v2 stores (e.g. C3ONTEXT) contain 0-dimensional arrays
    (``shape=()``, ``chunks=()``) whose ``_ARRAY_DIMENSIONS`` attribute lists
    one or more dimension names.  Since xarray 2024.9.0 the code that builds
    ``preferred_chunks`` uses ``zip(..., strict=True)``, which raises a
    ``ValueError`` when the lengths don't match.

    This patch catches that specific error and falls back to treating the array
    as a plain scalar variable with no dimension coordinates – the same
    (silent) behaviour that older xarray versions exhibited.

    The correct long-term fix is to regenerate the affected zarr stores so that
    every ``_ARRAY_DIMENSIONS`` entry matches the actual array shape.
    """
    try:
        from xarray.backends.zarr import ZarrStore, DIMENSION_KEY, ZarrArrayWrapper
        from xarray.core.variable import Variable
        from xarray.core import indexing
    except ImportError:
        return  # xarray not available; nothing to patch

    _orig = ZarrStore.open_store_variable

    def _patched(self, name):
        try:
            return _orig(self, name)
        except ValueError:
            # Re-raise unless this is the specific dimension/chunk length
            # mismatch that occurs for scalar zarr v2 arrays carrying
            # incorrect _ARRAY_DIMENSIONS metadata.
            zarr_array = self.members[name]
            dims_from_attrs = list(zarr_array.attrs.get(DIMENSION_KEY, []))
            chunks = zarr_array.chunks  # tuple, e.g. () for scalars
            if len(dims_from_attrs) != len(chunks):
                # This is the mismatch we expect; treat the array as a
                # dimension-less scalar and emit a warning so the issue is
                # visible in test output.
                warnings.warn(
                    f"Variable {name!r}: _ARRAY_DIMENSIONS {dims_from_attrs!r} "
                    f"does not match array shape {zarr_array.shape!r}. "
                    "Treating as a scalar. The zarr store should be regenerated "
                    "with correct metadata.",
                    UserWarning,
                    stacklevel=2,
                )
                data = indexing.LazilyIndexedArray(ZarrArrayWrapper(zarr_array))
                attributes = dict(zarr_array.attrs)
                attributes.pop(DIMENSION_KEY, None)
                encoding = {
                    "chunks": chunks,
                    "preferred_chunks": {},
                }
                return Variable(zarr_array.shape, data, attributes, encoding)
            raise

    ZarrStore.open_store_variable = _patched


# Apply the patch once at import time so it is active for the whole test session.
_patch_zarr_scalar_dimension_handling()

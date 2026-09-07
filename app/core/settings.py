"""Application settings compatibility exports.

The concrete settings implementation lives in :mod:`app.core.config` so
existing imports remain stable while callers can use the conventional module
name as well.
"""

from app.core.config import Settings, get_settings

__all__ = ["Settings", "get_settings"]
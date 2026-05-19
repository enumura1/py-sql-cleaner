from __future__ import annotations

from collections.abc import Callable

SqlFormatter = Callable[[str, str, str], str]

"""Search query helpers."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List, Optional

from .models import Photo


@dataclass
class SearchFilters:
    text: Optional[str] = None
    tags: Optional[list[int]] = None
    persons: Optional[list[int]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    favorites_only: bool = False
    root_ids: Optional[list[int]] = None
    limit: int = 200
    offset: int = 0


def query_photos(filters: SearchFilters) -> List[Photo]:
    """Placeholder query; integrate with DB layer later."""
    _ = filters
    return []

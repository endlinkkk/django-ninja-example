from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Product:
    id: int | None = field(default=None, kw_only=True)
    title: str
    description: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime | None = field(default=None)

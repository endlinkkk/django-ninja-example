from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Customer:
    id: int | None = field(default=None, kw_only=True)
    phone: str
    created_at: datetime

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:
    oid: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime

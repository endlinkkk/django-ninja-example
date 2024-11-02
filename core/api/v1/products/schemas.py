from datetime import datetime
from pydantic import BaseModel

from core.apps.products.entities.products import Product as ProductEntity


class ProductInSchema(BaseModel):
    title: str
    description: str

    def to_entity(self) -> ProductEntity:
        return ProductEntity(
            title=self.title,
            description=self.description,
        )


class ProductSchema(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: ProductEntity) -> "ProductSchema":
        return ProductSchema(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


ProductListSchema = list[ProductSchema]

from datetime import datetime
from pydantic import BaseModel

from core.apps.products.entities.reviews import Review as ReviewEntity


class ReviewInSchema(BaseModel):
    rating: int
    text: str

    def to_entity(self) -> ReviewEntity:
        return ReviewEntity(
            text=self.text,
            rating=self.rating,
        )


class CreateReviewSchema(BaseModel):
    product_id: int
    customer_token: str
    review: ReviewInSchema


class ReviewOutSchema(ReviewInSchema):
    id: int
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def from_entity(cls, review_entity: ReviewEntity):
        return cls(
            rating=review_entity.rating,
            text=review_entity.text,
            id=review_entity.id,
            created_at=review_entity.created_at,
            updated_at=review_entity.updated_at,
        )

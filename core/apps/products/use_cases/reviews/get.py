from dataclasses import dataclass

from core.apps.products.entities.reviews import Review as ReviewEntity
from core.apps.products.services.reviews import (
    BaseReviewService,
)


@dataclass
class GetReviewListUseCase:
    review_service: BaseReviewService

    def execute(
        self, product_id: int,
    ) -> list[ReviewEntity]:

        reviews = self.review_service.get_product_reviews(
            product_id=product_id
        )

        return reviews

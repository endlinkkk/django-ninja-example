from dataclasses import dataclass

from core.apps.customers.services.customers import BaseCustomerService
from core.apps.products.services.products import BaseProductService
from core.apps.products.services.reviews import (
    BaseReviewService,
    BaseReviewValidatorService,
)


@dataclass
class DeleteReviewUseCase:
    review_service: BaseReviewService
    customer_service: BaseCustomerService
    product_service: BaseProductService
    validator_service: BaseReviewValidatorService

    def execute(
        self,
        review_id: int,
        customer_token: str,
    ) -> None:
        customer = self.customer_service.get_by_token(token=customer_token)

        self.review_service.delete_review(review_id=review_id, customer=customer)

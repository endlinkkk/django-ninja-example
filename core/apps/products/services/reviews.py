from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.apps.customers.entities import Customer as CustomerEntity
from core.apps.products.entities.products import Product as ProductEntity
from core.apps.products.entities.reviews import Review as ReviewEntity
from core.apps.products.exceptions.reviews import (
    ReviewInvalidRating,
    ReviewNotFound,
    SingleReviewError,
)
from core.apps.products.models.reviews import Review as ReviewModel
from core.apps.customers.models import Customer as CustomerModel


@dataclass
class BaseReviewService(ABC):
    @abstractmethod
    def check_review_exists(
        self, product: ProductEntity, customer: CustomerEntity
    ) -> bool: ...
    @abstractmethod
    def save_review(
        self, customer: CustomerEntity, product: ProductEntity, review: ReviewEntity
    ) -> ReviewEntity: ...

    @abstractmethod
    def get_product_reviews(self, product_id: int) -> list[ReviewEntity]: ...

    @abstractmethod
    def delete_review(self, review_id: int, customer: CustomerEntity) -> None: ...


@dataclass
class ReviewService(BaseReviewService):
    def check_review_exists(
        self, product: ProductEntity, customer: CustomerEntity
    ) -> bool:
        return ReviewModel.objects.filter(
            product_id=product.id,
            customer_id=customer.id,
        ).exists()

    def save_review(
        self, customer: CustomerEntity, product: ProductEntity, review: ReviewEntity
    ) -> ReviewEntity:
        review_dto = ReviewModel.from_entity(
            review=review, product=product, customer=customer
        )
        review_dto.save()
        return review_dto.to_entity()

    def get_product_reviews(self, product_id: int) -> list[ReviewEntity]:
        reviews = ReviewModel.objects.filter(product__id=product_id)
        return [review.to_entity() for review in reviews]

    def delete_review(self, customer: CustomerEntity, review_id: int) -> None:
        try:
            customer_dto = CustomerModel.objects.get(pk=customer.id)
            review = ReviewModel.objects.get(pk=review_id, customer=customer_dto)
            review.delete()
        except ReviewModel.DoesNotExist:
            raise ReviewNotFound(review_id=review_id)


@dataclass
class BaseReviewValidatorService(ABC):
    @abstractmethod
    def validate(
        self,
        review: ReviewEntity,
        customer: CustomerEntity | None = None,
        product: ProductEntity | None = None,
    ): ...


class ReviewRatingValidatorService(BaseReviewValidatorService):
    def validate(self, review: ReviewEntity, *args, **kwargs):
        if not (1 <= review.rating <= 5):
            raise ReviewInvalidRating(rating=review.rating)


@dataclass
class SingleReviewValidatorService(BaseReviewValidatorService):
    service: BaseReviewService

    def validate(
        self,
        customer: CustomerEntity,
        product: ProductEntity,
        *args,
        **kwargs,
    ):
        if self.service.check_review_exists(product=product, customer=customer):
            raise SingleReviewError(product_id=product.id, customer_id=customer.id)


@dataclass
class ComposedReviewValidatorService:
    validators: list[BaseReviewValidatorService]

    def validate(
        self,
        review: ReviewEntity,
        customer: CustomerEntity | None = None,
        product: ProductEntity | None = None,
    ):
        for validator in self.validators:
            validator.validate(review=review, customer=customer, product=product)

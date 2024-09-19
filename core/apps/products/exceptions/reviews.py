from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class ReviewInvalidRating(ServiceException):
    rating: int

    @property
    def message(self):
        return "Rating is not valid"


@dataclass
class SingleReviewError(ServiceException):
    product_id: int
    customer_id: int

    @property
    def message(self):
        return 'The user already posted a review'
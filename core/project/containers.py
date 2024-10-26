from functools import lru_cache

import punq

from core.apps.customers.services.auth import AuthService, BaseAuthService
from core.apps.customers.services.codes import BaseCodeService, DjangoCacheCodeService
from core.apps.customers.services.customers import (
    BaseCustomerService,
    ORMCustomerService,
)
from core.apps.customers.services.senders import (
    BaseSenderService,
    ComposeSenderService,
    DummySenderService,
    EmailSenderService,
)
from core.apps.products.services.products import BaseProductService, BaseProductValidatorService, ComposedProductValidatorService, ORMProductService, ProductDescriptionValidatorService, ProductTitleValidatorService
from core.apps.products.services.reviews import (
    BaseReviewService,
    BaseReviewValidatorService,
    ComposedReviewValidatorService,
    ReviewRatingValidatorService,
    ReviewService,
    SingleReviewValidatorService,
)
from core.apps.products.use_cases.products.create import CreateProductUseCase
from core.apps.products.use_cases.reviews.create import CreateReviewUseCase
from core.apps.products.use_cases.products.delete import DeleteProductUseCase
from core.apps.products.use_cases.reviews.get import GetReviewListUseCase


@lru_cache(1)
def get_container():
    return _init_container()


def _init_container() -> punq.Container:
    



    container = punq.Container()

    # Products
    container.register(BaseProductService, ORMProductService)

    container.register(ProductTitleValidatorService)
    container.register(ProductDescriptionValidatorService)

    def build_product_validators() -> BaseProductValidatorService:
        return ComposedProductValidatorService(
            validators=[
                container.resolve(ProductTitleValidatorService),
                container.resolve(ProductDescriptionValidatorService),
            ]
        )
    
    container.register(
            BaseProductValidatorService, factory=build_product_validators
        )
    
    container.register(CreateProductUseCase)
    container.register(DeleteProductUseCase)


    # Customers
    container.register(BaseCustomerService, ORMCustomerService)
    container.register(
        BaseSenderService,
        ComposeSenderService,
        sender_services=[DummySenderService(), EmailSenderService()],
    )
    container.register(BaseCodeService, DjangoCacheCodeService)
    container.register(BaseAuthService, AuthService)
    container.register(BaseReviewService, ReviewService)
    
    container.register(SingleReviewValidatorService)
    container.register(ReviewRatingValidatorService)


    def build_review_validators() -> BaseReviewValidatorService:
        return ComposedReviewValidatorService(
            validators=[
                container.resolve(SingleReviewValidatorService),
                container.resolve(ReviewRatingValidatorService)
            ]
        )
    


    container.register(
            BaseReviewValidatorService, factory=build_review_validators
        )
    
    container.register(CreateReviewUseCase)
    container.register(GetReviewListUseCase)

    return container

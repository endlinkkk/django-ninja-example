from dataclasses import dataclass

from core.apps.customers.services.customers import BaseCustomerService
from core.apps.products.entities.products import Product as ProductEntity
from core.apps.products.services.products import BaseProductService
from core.apps.products.services.products import (
    BaseProductValidatorService,
)


@dataclass
class CreateProductUseCase:
    product_service: BaseProductService
    customer_service: BaseCustomerService
    validator_service: BaseProductValidatorService

    def execute(
        self, product: ProductEntity, customer_token: str,
    ) -> ProductEntity:
        self.customer_service.get_by_token(token=customer_token)

        self.validator_service.validate(
            product=product
        )
        
        saved_product = self.product_service.add_product(product=product)

        return saved_product

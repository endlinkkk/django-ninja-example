from dataclasses import dataclass

from core.apps.customers.services.customers import BaseCustomerService
from core.apps.products.services.products import BaseProductService


@dataclass
class DeleteProductUseCase:
    product_service: BaseProductService
    customer_service: BaseCustomerService

    def execute(
        self,
        product_id: int,
        customer_token: str,
    ) -> None:
        self.customer_service.get_by_token(token=customer_token)

        self.product_service.delete_product(product_id=product_id)

from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class ProductNotFound(ServiceException):
    product_id: int

    @property
    def message(self):
        return "A product with product id is not found"


@dataclass(eq=False)
class ProductInvalidTitle(ServiceException):
    title: str

    @property
    def message(self):
        return "A product title is too long"


@dataclass(eq=False)
class ProductInvalidDescription(ServiceException):
    description: str

    @property
    def message(self):
        return "A product description is too long"

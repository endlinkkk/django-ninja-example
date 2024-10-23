from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.products.filters import ProductFilters
from core.apps.products.entities.products import Product as ProductEntity
from core.apps.products.exceptions.products import ProductInvalidDescription, ProductInvalidTitle, ProductNotFound
from core.apps.products.models.products import Product as ProductModel


@dataclass
class BaseProductService(ABC):
    @abstractmethod
    def get_product_list(
        self, filters: ProductFilters, pagination: PaginationIn
    ) -> Iterable[ProductEntity]: ...

    @abstractmethod
    def get_product_count(self, filters: ProductFilters) -> int: ...

    @abstractmethod
    def get_by_product_id(self, product_id) -> ProductEntity: ...

    @abstractmethod
    def add_product(self, product: ProductEntity) -> ProductEntity: ...


@dataclass
class BaseProductValidatorService(ABC):
    @abstractmethod
    def validate(
        self,
        product: ProductEntity,
    ): ...


@dataclass
class ProductTitleValidatorService(BaseProductValidatorService):
    def validate(self, product: ProductEntity):
        if len(product.title) > 255:
            raise ProductInvalidTitle(title=product.title)


@dataclass
class ProductDescriptionValidatorService(BaseProductValidatorService):
    def validate(self, product: ProductEntity):
        if len(product.description) > 1000:
            raise ProductInvalidDescription(description=product.description)


@dataclass
class ComposedProductValidatorService:
    validators: list[BaseProductValidatorService]

    def validate(
        self,
        product: ProductEntity,
    ):
        for validator in self.validators:
            validator.validate(product=product)


@dataclass
class ORMProductService(BaseProductService):
    def _build_get_product_query(self, filters: ProductFilters) -> Q:
        query = Q(is_active=True)

        if filters.search is not None:
            query &= Q(title__icontains=filters.search) | Q(
                description__icontains=filters.search
            )

        return query

    def get_product_list(
        self, filters: ProductFilters, pagination: PaginationIn
    ) -> Iterable[ProductEntity]:
        query = self._build_get_product_query(filters=filters)

        qs = ProductModel.objects.filter(query)[
            pagination.offset : pagination.offset + pagination.limit
        ]

        return [product.to_entity() for product in qs]

    def get_product_count(self, filters: ProductFilters) -> int:
        query = self._build_get_product_query(filters=filters)
        return ProductModel.objects.filter(query).count()

    def get_by_product_id(self, product_id) -> ProductEntity:
        try:
            product_dto = ProductModel.objects.get(pk=product_id)
        except ProductModel.DoesNotExist:
            raise ProductNotFound(product_id=product_id)

        return product_dto.to_entity()
    

    def add_product(self, product) -> ProductEntity:
        product_dto = ProductModel.objects.create(title=product.title, description=product.description)
        return product_dto.to_entity()
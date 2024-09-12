from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.products.filters import ProductFilters
from core.apps.products.entities.products import Product
from core.apps.products.models.products import Product as ProductModel


@dataclass
class BaseProductService(ABC):
    @abstractmethod
    def get_product_list(
        self, filters: ProductFilters, pagination: PaginationIn
    ) -> Iterable[Product]: ...

    @abstractmethod
    def get_product_count(self, filters: ProductFilters) -> int: ...


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
    ) -> Iterable[Product]:
        query = self._build_get_product_query(filters=filters)

        qs = ProductModel.objects.filter(query)[
            pagination.offset : pagination.offset + pagination.limit
        ]

        return [product.to_entity() for product in qs]

    def get_product_count(self, filters: ProductFilters) -> int:
        query = self._build_get_product_query(filters=filters)
        return ProductModel.objects.filter(query).count()

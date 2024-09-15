import pytest

from core.api.filters import PaginationIn
from core.api.v1.products.filters import ProductFilters
from core.apps.products.services.products import BaseProductService
from tests.factories.products import ProductModelFactory


def generate_products(products_count: int):
    return ProductModelFactory.create_batch(size=products_count)


@pytest.mark.django_db
def test_products_count_zero(product_service: BaseProductService):
    products_count = product_service.get_product_count(ProductFilters())
    assert products_count == 0, products_count


@pytest.mark.skip
def test_product_search():
    assert True


@pytest.mark.django_db
def test_get_products_count_exists(product_service: BaseProductService):
    expected_products_count = 5
    generate_products(expected_products_count)

    products_count = product_service.get_product_count(ProductFilters())
    assert products_count == expected_products_count, products_count


@pytest.mark.django_db
def test_get_products_all(product_service: BaseProductService):
    expected_products_count = 5
    products = generate_products(expected_products_count)

    products_titles = {product.title for product in products}

    fetched_products = product_service.get_product_list(
        ProductFilters(), PaginationIn()
    )

    fetched_titles = {product.title for product in fetched_products}

    assert len(products_titles) == len(fetched_titles)
    assert fetched_titles == products_titles

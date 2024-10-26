from django.http import HttpRequest, HttpResponse
from ninja import Header, Query, Router
from ninja.errors import HttpError

from core.api.filters import PaginationIn
from core.api.schemas import ApiResponse, ListPaginatedResponse, PaginationOut
from core.api.v1.products.filters import ProductFilters
from core.api.v1.products.schemas import ProductInSchema, ProductSchema
from core.apps.common.exceptions import ServiceException
from core.apps.products.filters.products import ProductFilters as ProductFiltersEntity
from core.apps.products.services.products import BaseProductService
from core.apps.products.use_cases.products.create import CreateProductUseCase
from core.apps.products.use_cases.products.delete import DeleteProductUseCase
from core.project.containers import get_container

router = Router(tags=["Products"])


@router.get("", response=ApiResponse[ListPaginatedResponse[ProductSchema]])
def get_product_list_handler(
    request: HttpRequest,
    filters: Query[ProductFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[ProductSchema]]:
    container = get_container()
    service: BaseProductService = container.resolve(BaseProductService)

    product_list = service.get_product_list(
        filters=ProductFiltersEntity(search=filters.search), pagination=pagination_in
    )
    product_count = service.get_product_count(filters=filters)

    items = [ProductSchema.from_entity(obj) for obj in product_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=product_count,
    )

    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out)
    )


@router.post("", response=ApiResponse[ProductSchema])
def create_product_handler(
    request: HttpRequest,
    schema: ProductInSchema,
    token: str = Header(alias="Auth-Token"),
) -> ApiResponse[ProductSchema]:
        container = get_container()
        use_case: CreateProductUseCase = container.resolve(CreateProductUseCase)
        try:
            result = use_case.execute(
                product=schema.to_entity(), customer_token=token,
            )
        except ServiceException as err:
            raise HttpError(status_code=400, message=err.message)

        return ApiResponse(data=ProductSchema.from_entity(result))



@router.delete("", response=None)
def delete_product_handler(
    request: HttpRequest,
    product_id: int,
    token: str = Header(alias="Auth-Token"),
) -> HttpResponse:
        container = get_container()
        use_case: DeleteProductUseCase = container.resolve(DeleteProductUseCase)
        try:
            use_case.execute(
                product_id=product_id, customer_token=token,
            )
        except ServiceException as err:
            raise HttpError(status_code=400, message=err.message)

        return HttpResponse(status=204)
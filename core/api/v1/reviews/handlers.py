from django.http import HttpRequest
from ninja import Header, Router, Query
from ninja.errors import HttpError
from core.api.filters import PaginationIn, PaginationOut
from core.api.schemas import ApiResponse, ListPaginatedResponse

from core.api.v1.reviews.schemas import (
    ReviewInSchema,
    ReviewOutSchema,
)
from core.apps.common.exceptions import ServiceException
from core.apps.products.use_cases.reviews.create import CreateReviewUseCase
from core.apps.products.use_cases.reviews.get import GetReviewListUseCase
from core.project.containers import get_container

router = Router(tags=["Reviews"])


@router.post(
    "/{product_id}/reviews",
    response=ApiResponse[ReviewOutSchema],
    operation_id="createReview",
)
def create_review(
    request: HttpRequest,
    product_id: int,
    schema: ReviewInSchema,
    token: str = Header(alias="Auth-Token"),
) -> ApiResponse[ReviewOutSchema]:
    container = get_container()
    use_case: CreateReviewUseCase = container.resolve(CreateReviewUseCase)
    try:
        result = use_case.execute(
            product_id=product_id, customer_token=token, review=schema.to_entity()
        )
    except ServiceException as err:
        raise HttpError(status_code=400, message=err.message)

    return ApiResponse(data=ReviewOutSchema.from_entity(result))


@router.get(
    "/{product_id}/reviews",
    response=ApiResponse[ListPaginatedResponse[ReviewOutSchema]],
    operation_id="getListReview",
)
def get_review_list_handler(
    request: HttpRequest,
    product_id: int,
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[ReviewOutSchema]]:
    container = get_container()
    use_case: GetReviewListUseCase = container.resolve(GetReviewListUseCase)
    try:
        review_list = use_case.execute(
            product_id=product_id
        )
        items = [ReviewOutSchema.from_entity(obj) for obj in review_list]
        pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=len(items),
    )
    except ServiceException as err:
        raise HttpError(status_code=400, message=err.message)

    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out)
    )




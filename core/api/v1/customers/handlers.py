from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError


from core.api.schemas import ApiResponse
from core.api.v1.customers.schemas import (
    AuthInSchema,
    AuthOutSchema,
    TokenInSchema,
    TokenOutSchema,
)
from core.apps.common.exceptions import ServiceException
from core.apps.customers.services.auth import BaseAuthService
from core.project.containers import get_container


router = Router(tags=["Customers"])


@router.post("auth", response=ApiResponse[AuthOutSchema], operation_id="authorize")
def auth_handler(
    request: HttpRequest,
    schema: AuthInSchema,
) -> ApiResponse[AuthOutSchema]:
    container = get_container()
    service = container.resolve(BaseAuthService)

    service.authorize(phone=schema.phone)
    return ApiResponse(data=AuthOutSchema(message=f"Code is sent to {schema.phone}"))


@router.post(
    "confirm", response=ApiResponse[TokenOutSchema], operation_id="confirm-code"
)
def get_token(
    request: HttpRequest,
    schema: TokenInSchema,
) -> ApiResponse[TokenOutSchema]:
    container = get_container()
    service = container.resolve(BaseAuthService)
    try:
        token = service.confirm(phone=schema.phone, code=schema.code)
    except ServiceException as e:
        raise HttpError(status_code=400, message=e.message)
    return ApiResponse(data=TokenOutSchema(token=token))

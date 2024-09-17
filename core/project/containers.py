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
from core.apps.products.services.products import BaseProductService, ORMProductService


@lru_cache(1)
def get_container():
    return _init_container()


def _init_container() -> punq.Container:
    container = punq.Container()

    # Products
    container.register(BaseProductService, ORMProductService)

    # Customers
    container.register(BaseCustomerService, ORMCustomerService)
    container.register(
        BaseSenderService,
        ComposeSenderService,
        sender_services=[DummySenderService(), EmailSenderService()],
    )
    container.register(BaseCodeService, DjangoCacheCodeService)
    container.register(BaseAuthService, AuthService)

    return container

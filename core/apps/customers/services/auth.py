from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.apps.customers.services.codes import BaseCodeService
from core.apps.customers.services.customers import BaseCustomerService
from core.apps.customers.services.senders import BaseSenderService


@dataclass(eq=False)
class BaseAuthService(ABC):
    customer_service: BaseCustomerService
    code_service: BaseCodeService
    sender_service: BaseSenderService

    @abstractmethod
    def authorize(self, phone: str): ...

    @abstractmethod
    def confirm(self, code: str, phone: str): ...


@dataclass
class AuthService(BaseAuthService):
    def authorize(self, phone: str):
        customer = self.customer_service.get_or_create(phone=phone)
        code = self.code_service.generate_code(customer=customer)
        self.sender_service.send_code(customer, code)

    def confirm(self, code: str, phone: str):
        customer = self.customer_service.get(phone)
        self.code_service.validate_code(code, customer)
        return self.customer_service.generate_token(customer)

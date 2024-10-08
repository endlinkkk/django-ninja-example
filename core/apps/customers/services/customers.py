from dataclasses import dataclass
from abc import ABC, abstractmethod
from uuid import uuid4

from core.apps.customers.entities import Customer
from core.apps.customers.exceptions.customers import CustomerTokenInvalid
from core.apps.customers.models import Customer as CustomerModel


@dataclass
class BaseCustomerService(ABC):
    @abstractmethod
    def get_or_create(self, phone: str) -> Customer: ...

    @abstractmethod
    def generate_token(self, customer: Customer) -> str: ...

    @abstractmethod
    def get(self, phone: str) -> Customer: ...

    @abstractmethod
    def get_by_token(self, token: str) -> Customer: ...


@dataclass
class ORMCustomerService(BaseCustomerService):
    def get_or_create(self, phone: str) -> Customer:
        customer_dto, _ = CustomerModel.objects.get_or_create(phone=phone)
        return customer_dto.to_entity()

    def get(self, phone: str) -> Customer:
        customer_dto = CustomerModel.objects.get(phone=phone)
        return customer_dto.to_entity()

    def generate_token(self, customer: Customer) -> str:
        token = str(uuid4())
        CustomerModel.objects.filter(phone=customer.phone).update(token=token)
        return token

    def get_by_token(self, token: str) -> Customer:
        try:
            customer_dto = CustomerModel.objects.get(token=token)
        except CustomerModel.DoesNotExist:
            raise CustomerTokenInvalid(token=token)

        return customer_dto.to_entity()

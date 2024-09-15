from dataclasses import dataclass
from abc import ABC, abstractmethod
from uuid import uuid4

from core.apps.customers.entities import CustomerEntity
from core.apps.customers.models import Customer as CustomerModel


@dataclass
class BaseCustomerService(ABC):
    @abstractmethod
    def get_or_create(self, phone: str) -> CustomerEntity: ...

    @abstractmethod
    def generate_token(self, customer: CustomerEntity) -> str: ...

    @abstractmethod
    def get(self, phone: str) -> CustomerEntity: ...


@dataclass
class ORMCustomerService(BaseCustomerService):
    def get_or_create(self, phone: str) -> CustomerEntity:
        customer_dto, _ = CustomerModel.objects.get_or_create(phone=phone)
        return customer_dto.to_entity()

    def get(self, phone: str) -> CustomerEntity:
        user_dto = CustomerModel.objects.get(phone=phone)
        return user_dto.to_entity()

    def generate_token(self, customer: CustomerEntity) -> str:
        token = str(uuid4())
        CustomerModel.objects.filter(phone=customer.phone).update(token=token)
        return token

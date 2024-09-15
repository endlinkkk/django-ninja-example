from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.apps.customers.entities import CustomerEntity


@dataclass
class BaseSenderService(ABC):
    @abstractmethod
    def send_code(self, customer: CustomerEntity, code: str) -> None: ...


@dataclass
class DummySenderService(BaseSenderService):
    def send_code(self, customer: CustomerEntity, code: str) -> None:
        print(f"Code sent: {code=}\nTo customer: {customer=}")

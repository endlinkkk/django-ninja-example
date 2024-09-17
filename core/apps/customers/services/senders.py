from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.apps.customers.entities import Customer


@dataclass
class BaseSenderService(ABC):
    @abstractmethod
    def send_code(self, customer: Customer, code: str) -> None: ...


@dataclass
class DummySenderService(BaseSenderService):
    def send_code(self, customer: Customer, code: str) -> None:
        print(f"Code sent: {code=}\nTo customer: {customer=}")


@dataclass
class EmailSenderService(BaseSenderService):
    def send_code(self, customer: Customer, code: str) -> None:
        print(f"Code sent: {code}\nTo customer email: {customer}")


@dataclass
class ComposeSenderService(BaseSenderService):
    sender_services: list[BaseSenderService]

    def send_code(self, customer: Customer, code: str) -> None:
        for service in self.sender_services:
            service.send_code(customer, code)

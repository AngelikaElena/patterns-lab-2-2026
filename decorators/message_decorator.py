"""
Базовый Decorator и конкретные декораторы необходимо реализовать самостоятельно.

Подсказка: все декораторы должны удовлетворять интерфейсу BaseMessage и
работать с другим объектом BaseMessage через композицию.
"""

# TODO:
# - MessageDecorator
# - HeaderDecorator
# - SignatureDecorator
# - DateDecorator
# - Base64Decorator

import base64
from datetime import datetime
from interfaces import BaseMessage


class MessageDecorator(BaseMessage):
    """
    Базовый класс декоратора.
    Реализует тот же интерфейс BaseMessage и хранит ссылку на оборачиваемый объект.
    """
    def __init__(self, message: BaseMessage) -> None:
        self._message = message

    def render(self) -> str:
        # По умолчанию просто делегирует вызов внутреннему объекту
        return self._message.render()


class HeaderDecorator(MessageDecorator):
    def __init__(self, message: BaseMessage, header: str) -> None:
        super().__init__(message)
        self._header = header

    def render(self) -> str:
        # Получаем текст и добавляем заголовок ПЕРЕД ним
        return f"{self._header}\n{self._message.render()}"


class SignatureDecorator(MessageDecorator):
    def __init__(self, message: BaseMessage, signature: str) -> None:
        super().__init__(message)
        self._signature = signature

    def render(self) -> str:
        # Получаем текст и добавляем подпись ПОСЛЕ него
        return f"{self._message.render()}\n\n{self._signature}"


class DateDecorator(MessageDecorator):
    def __init__(self, message: BaseMessage, date_format: str = "%d.%m.%Y") -> None:
        super().__init__(message)
        # Берем текущую дату при создании декоратора
        self._date_str = datetime.now().strftime(date_format)

    def render(self) -> str:
        # Добавляем дату после сообщения
        return f"{self._message.render()}\n\nДата: {self._date_str}"


class Base64Decorator(MessageDecorator):
    def render(self) -> str:
        # Получаем итоговый текст из всех внутренних декораторов
        raw_text = self._message.render()
        # Кодируем в байты (UTF-8), затем в Base64, затем обратно в строку
        encoded_bytes = base64.b64encode(raw_text.encode("utf-8"))
        return encoded_bytes.decode("utf-8")
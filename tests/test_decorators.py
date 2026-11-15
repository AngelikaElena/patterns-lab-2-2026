import base64
from messages import Message
from decorators import (
    MessageDecorator,
    HeaderDecorator,
    SignatureDecorator,
    DateDecorator,
    Base64Decorator,
)


def test_message_decorator_delegates_render() -> None:
    """Базовый декоратор должен просто возвращать текст обернутого сообщения."""
    base = Message("hello")
    decorator = MessageDecorator(base)
    assert decorator.render() == "hello"


def test_header_decorator() -> None:
    """HeaderDecorator добавляет заголовок перед текстом."""
    base = Message("hello")
    decorator = HeaderDecorator(base, header="TITLE")
    assert decorator.render() == "TITLE\nhello"


def test_signature_decorator() -> None:
    """SignatureDecorator добавляет подпись после текста."""
    base = Message("hello")
    decorator = SignatureDecorator(base, signature="--- John Doe")
    assert decorator.render() == "hello\n\n--- John Doe"


def test_date_decorator() -> None:
    """DateDecorator добавляет дату после текста."""
    base = Message("hello")
    decorator = DateDecorator(base)
    result = decorator.render()
    # Так как дата зависит от текущего дня, проверяем только наличие "Дата:"
    # и исходного текста
    assert "hello" in result
    assert "Дата: " in result


def test_base64_decorator() -> None:
    """Base64Decorator кодирует текст в Base64."""
    base = Message("secret")
    decorator = Base64Decorator(base)
    result = decorator.render()
    
    # Проверяем, что это валидный Base64 и декодируется обратно в "secret"
    decoded_bytes = base64.b64decode(result.encode("utf-8"))
    assert decoded_bytes.decode("utf-8") == "secret"


def test_decorator_combination() -> None:
    """Проверяем, что декораторы свободно комбинируются."""
    base = Message("hello")
    
    # Собираем цепочку: Header -> Signature -> Base64
    # Сначала подпись, потом заголовок, потом Base64.
    chain = Base64Decorator(
        HeaderDecorator(
            SignatureDecorator(base, signature="SIGN"),
            header="HEAD"
        )
    )
    
    result = chain.render()
    
    # Ожидаемый текст до кодирования: "HEAD\nhello\n\nSIGN"
    expected_raw = "HEAD\nhello\n\nSIGN"
    decoded_bytes = base64.b64decode(result.encode("utf-8"))
    assert decoded_bytes.decode("utf-8") == expected_raw
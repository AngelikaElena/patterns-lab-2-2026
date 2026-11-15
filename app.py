from messages import Message
from decorators import (
    HeaderDecorator,
    SignatureDecorator,
    DateDecorator,
    Base64Decorator,
)
from proxies import ProtectedMessageProxy
from security import UserContext


def main() -> None:
    # ==========================================
    # ЧАСТЬ 1: ДЕМОНСТРАЦИЯ РАБОТЫ ДЕКОРАТОРОВ
    # ==========================================
    
    # 1. Базовое сообщение
    base_message = Message("С наступающим Новым годом!")
    print("--- 0. Исходное сообщение ---")
    print(base_message.render())
    print()

    # 2. Собираем текстовую цепочку (без Base64)
    # Порядок вложенности: Signature -> Date -> Header
    text_message = HeaderDecorator(
        DateDecorator(
            SignatureDecorator(base_message, signature="С уважением, Мария")
        ),
        header="=== ВАЖНОЕ УВЕДОМЛЕНИЕ ==="
    )

    print("--- 1. Результат работы текстовых декораторов ---")
    print(text_message.render())
    print()

    # 3. Оборачиваем всю цепочку в Base64Decorator
    base64_message = Base64Decorator(text_message)
    
    print("--- 2. Результат работы Base64Decorator ---")
    print(base64_message.render())
    print()

    # ==========================================
    # ЧАСТЬ 2: ДЕМОНСТРАЦИЯ РАБОТЫ ПРОКСИ (PROXY)
    # ==========================================
    
    print("--- 3. Демонстрация работы Proxy ---")
    
    # Создаем пользователей
    admin_user = UserContext.of("Alice", "admin", "user")
    guest_user = UserContext.of("Bob", "guest")

    # Оборачиваем наше текстовое сообщение в Прокси (требуем роль "admin")
    # Для удобства чтения передаем text_message, а не base64_message
    proxy = ProtectedMessageProxy(
        message=text_message,
        user=admin_user,
        required_role="admin"
    )

    # Попытка 1: Успешный доступ (пользователь Alice - admin)
    print(f"[Успешный доступ] Пользователь: {admin_user.username}")
    try:
        print(proxy.render())
    except PermissionError as e:
        print(f"Ошибка: {e}")
    print()

    # Попытка 2: Отказ в доступе (пользователь Bob - guest)
    # Создаем новый Прокси с тем же сообщением, но для Bob'а
    proxy_for_guest = ProtectedMessageProxy(
        message=text_message,
        user=guest_user,
        required_role="admin"
    )
    
    print(f"[Отказ в доступе] Пользователь: {guest_user.username}")
    try:
        print(proxy_for_guest.render())
    except PermissionError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
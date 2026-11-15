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
    # --- ЧАСТЬ 1: ДЕКОРАТОРЫ ---
    base_message = Message("С наступающим Новым годом!")
    
    # Собираем красивую цепочку декораторов
    decorated_message = HeaderDecorator(
        DateDecorator(
            SignatureDecorator(base_message, signature="С уважением, Мария")
        ),
        header="=== ВАЖНОЕ УВЕДОМЛЕНИЕ ==="
    )

    print("--- 1. Результат работы декораторов ---")
    print(decorated_message.render())
    print()

    # --- ЧАСТЬ 2: ПРОКСИ (ЗАЩИТА ДОСТУПА) ---
    print("--- 2. Демонстрация работы Proxy ---")
    
    # Создаем пользователей
    admin_user = UserContext.of("Alice", "admin", "user")
    guest_user = UserContext.of("Bob", "guest")

    # Оборачиваем наше красивое сообщение в Прокси (требуем роль "admin")
    proxy = ProtectedMessageProxy(
        message=decorated_message,
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
    # Для этого создаем новый Прокси с тем же сообщением, но для Bob'а
    proxy_for_guest = ProtectedMessageProxy(
        message=decorated_message,
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
import pytest
from messages import Message
from proxies import ProtectedMessageProxy
from security import UserContext


def test_proxy_allows_access_with_correct_role() -> None:
    """Прокси должен разрешить рендер, если у пользователя есть нужная роль."""
    base = Message("Top secret")
    user = UserContext.of("Alice", "admin", "user")
    
    proxy = ProtectedMessageProxy(
        message=base,
        user=user,
        required_role="admin"
    )
    
    # Если роль есть, метод render должен вернуть текст без изменений
    assert proxy.render() == "Top secret"


def test_proxy_denies_access_without_role() -> None:
    """Прокси должен выбросить PermissionError, если роли нет."""
    base = Message("Top secret")
    user = UserContext.of("Bob", "guest") # У Боба нет роли admin
    
    proxy = ProtectedMessageProxy(
        message=base,
        user=user,
        required_role="admin"
    )
    
    # Используем pytest.raises, чтобы проверить, что выбрасывается ошибка
    with pytest.raises(PermissionError):
        proxy.render()
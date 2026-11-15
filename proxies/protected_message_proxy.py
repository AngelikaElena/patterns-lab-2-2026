"""
Реализуйте ProtectedMessageProxy.

Proxy должен предоставлять интерфейс BaseMessage, проверять AccessPolicy
и делегировать render() реальному объекту только при наличии доступа.
"""

# TODO: реализуйте ProtectedMessageProxy.

from interfaces import BaseMessage
from security import AccessPolicy, UserContext


class ProtectedMessageProxy(BaseMessage):
    """
    Защищающий Proxy.
    Не изменяет содержание сообщения, а контролирует доступ к вызову render().
    """

    def __init__(
        self, 
        message: BaseMessage, 
        user: UserContext, 
        required_role: str
    ) -> None:
        # 1. Храним ссылку на реальный объект сообщения
        self._message = message
        # 2. Храним контекст пользователя, который пытается получить доступ
        self._user = user
        # 3. Создаем политику доступа для требуемой роли
        self._access_policy = AccessPolicy(required_role)

    def render(self) -> str:
        # 4. Проверяем права доступа через AccessPolicy
        if not self._access_policy.is_allowed(self._user):
            # 5. Если прав нет — выбрасываем исключение
            raise PermissionError(
                f"Пользователь '{self._user.username}' не имеет необходимых прав "
                f"для просмотра сообщения."
            )
        
        # 6. Если права есть — просто делегируем вызов реальному объекту
        # (никакой логики форматирования текста здесь нет!)
        return self._message.render()
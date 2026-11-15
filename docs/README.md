# Диаграмма

Поместите сюда структурную диаграмму, на которой отдельно видны:

- базовый компонент;
- Decorator и конкретные декораторы;
- Proxy;
- реальный субъект, к которому Proxy контролирует доступ.

# Диаграмма классов

Структурная диаграмма проекта, отображающая базовый компонент, Декораторы, Прокси, реальный субъект и контроль доступа.

```mermaid
classDiagram
    %% Базовый компонент
    class BaseMessage {
        <<interface>>
        +render() str
    }

    %% Реальный субъект (Базовое сообщение)
    class Message {
        -text: str
        +render() str
    }

    %% Базовый декоратор и конкретные декораторы
    class MessageDecorator {
        #message: BaseMessage
        +render() str
    }

    class HeaderDecorator {
        -header: str
        +render() str
    }
    class SignatureDecorator {
        -signature: str
        +render() str
    }
    class DateDecorator {
        -date_format: str
        +render() str
    }
    class Base64Decorator {
        +render() str
    }

    %% Прокси (Заместитель)
    class ProtectedMessageProxy {
        -message: BaseMessage
        -user: UserContext
        -access_policy: AccessPolicy
        +render() str
    }

    %% Вспомогательные классы безопасности
    class AccessPolicy {
        -required_role: str
        +is_allowed(user: UserContext) bool
    }

    class UserContext {
        +username: str
        +roles: frozenset
    }

    %% Связи
    BaseMessage <|.. Message : реализует
    BaseMessage <|.. MessageDecorator : реализует
    BaseMessage <|.. ProtectedMessageProxy : реализует

    %% Декоратор оборачивает BaseMessage (композиция)
    MessageDecorator o-- BaseMessage : оборачивает
    MessageDecorator <|-- HeaderDecorator : наследует
    MessageDecorator <|-- SignatureDecorator : наследует
    MessageDecorator <|-- DateDecorator : наследует
    MessageDecorator <|-- Base64Decorator : наследует

    %% Прокси контролирует доступ к реальному субъекту
    ProtectedMessageProxy o-- BaseMessage : контролирует доступ к (Реальный субъект)
    ProtectedMessageProxy --> AccessPolicy : использует
    AccessPolicy --> UserContext : проверяет
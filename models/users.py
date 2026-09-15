"""Класс пользователя и функции работы с коллекцией пользователей."""

from datetime import date

from utils import format_date, get_next_id

MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 30


class User:
    """Пользователь сервиса — владелец коротких ссылок."""

    def __init__(
        self,
        user_id: int,
        username: str,
        email: str,
        registered_at: date,
    ) -> None:
        """Создать объект пользователя."""
        self.id = user_id
        self.username = username
        self.email = email
        self.registered_at = registered_at

    def __str__(self) -> str:
        """Вернуть строковое представление пользователя."""
        return (
            f"#{self.id} {self.username} <{self.email}>, "
            f"с {format_date(self.registered_at)}"
        )

    @staticmethod
    def validate_email(email: str) -> bool:
        """Проверить, что адрес электронной почты имеет вид имя@домен."""
        name, separator, domain = email.partition("@")
        if not name or not separator or " " in email:
            return False
        return "." in domain and "@" not in domain

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из записи, прочитанной из JSON."""
        return cls(
            user_id=data["id"],
            username=data["username"],
            email=data["email"],
            registered_at=date.fromisoformat(data["registered_at"]),
        )


def add_user(
    users: list[User],
    username: str,
    email: str,
    registered_at: date,
) -> User:
    """Создать пользователя и добавить его в коллекцию users.

    Логин и адрес электронной почты должны быть уникальными.
    При некорректных данных возбуждается ValueError.
    """
    username = username.strip()
    email = email.strip().lower()
    has_valid_length = (
        MIN_USERNAME_LENGTH <= len(username) <= MAX_USERNAME_LENGTH
    )
    if not has_valid_length:
        raise ValueError(
            f"Логин должен содержать от {MIN_USERNAME_LENGTH} "
            f"до {MAX_USERNAME_LENGTH} символов"
        )
    if not User.validate_email(email):
        raise ValueError("Некорректный адрес электронной почты")
    for user in users:
        if user.username.lower() == username.lower():
            raise ValueError(f"Логин «{username}» уже занят")
        if user.email.lower() == email:
            raise ValueError(f"Адрес {email} уже используется")

    new_user = User(get_next_id(users), username, email, registered_at)
    users.append(new_user)
    return new_user


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    """Найти пользователя по идентификатору; вернуть None, если его нет."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_users(users: list[User], query: str) -> list[User]:
    """Найти пользователей по части логина или адреса электронной почты.

    Поиск выполняется без учёта регистра.
    """
    query = query.strip().lower()
    found = []
    for user in users:
        if query in user.username.lower() or query in user.email.lower():
            found.append(user)
    return found


def show_users(users: list[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Пользователи не найдены")
        return
    for user in users:
        print(user)

from datetime import date

from models import User
from models.users import add_user, find_user_by_id, find_users

REGISTERED_AT = date(2026, 9, 1)


def test_user_creation():
    user = User(1, "anna", "anna@example.com", REGISTERED_AT)
    assert user.id == 1
    assert user.username == "anna"
    assert user.email == "anna@example.com"


def test_user_str():
    user = User(1, "anna", "anna@example.com", REGISTERED_AT)
    assert str(user) == "#1 anna <anna@example.com>, с 01.09.2026"


def test_user_from_data():
    data = {
        "id": 2,
        "username": "ivan",
        "email": "ivan@example.com",
        "registered_at": "2026-08-20",
    }
    user = User.from_data(data)
    assert user.username == "ivan"
    assert user.registered_at == date(2026, 8, 20)


def test_email_without_at_is_invalid():
    assert not User.validate_email("anna.example.com")


def test_add_user_assigns_next_id():
    users = []
    add_user(users, "anna", "anna@example.com", REGISTERED_AT)
    user = add_user(users, "ivan", "ivan@example.com", REGISTERED_AT)
    assert user.id == 2


def test_find_users_by_email():
    users = []
    anna = add_user(users, "anna", "anna@example.com", REGISTERED_AT)
    add_user(users, "ivan", "ivan@example.com", REGISTERED_AT)
    assert find_users(users, "ANNA@") == [anna]


def test_find_user_by_unknown_id():
    users = []
    add_user(users, "anna", "anna@example.com", REGISTERED_AT)
    assert find_user_by_id(users, 99) is None

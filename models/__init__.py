"""Объектная модель сервиса сокращения ссылок."""

from .clicks import Click
from .links import Link
from .users import User

__all__ = ["Click", "Link", "User"]

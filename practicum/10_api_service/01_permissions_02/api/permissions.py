"""
В приложении **api** опишите и примените пермишен, который не даст пользователю
удалить или отредактировать чужие публикации.

Запрашивать список всех публикаций или отдельную публикацию может любой
пользователь. Создавать новую публикацию может только аутентифицированный
пользователь.
"""

from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )

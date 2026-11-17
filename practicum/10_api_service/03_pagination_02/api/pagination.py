"""
Измените используемую по умолчанию структуру ответа при пагинации. Уберите поля
`next` и `previous` из выдачи, а название ключа `results` измените на
`response`.

Создайте файл `pagination.py` в директории приложения `api` и опишите в нём
собственный пагинатор-класс `CustomPagination`.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "response": data,
            }
        )

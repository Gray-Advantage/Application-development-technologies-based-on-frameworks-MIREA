"""
Запретите любые запросы к публикациям в обеденное время (с 13:00 до 14:00).
Опишите в приложении **api** тротлинг-класс `LunchBreakThrottle` и подключите
его к соответствующему view-классу публикаций.

![](https://pictures.s3.yandex.net:443/resources/image_1708513946.png)
"""

import datetime

from rest_framework import throttling


class LunchBreakThrottle(throttling.BaseThrottle):

    def allow_request(self, request, view):
        return datetime.datetime.now().hour != 13

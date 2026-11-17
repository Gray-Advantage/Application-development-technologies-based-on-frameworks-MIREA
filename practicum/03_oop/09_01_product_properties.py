"""Реализуйте Product с атрибутами name, retail_price и purchase_price.

Свойство profit возвращает разницу розничной и закупочной цены.
Статический метод average_price(prices) возвращает среднее значение списка
розничных цен; при вызове без аргументов возвращает 0.
Свойство information возвращает строку в формате:
название – Шляпа, розничная цена – 1000, закупочная цена – 800
Сохраните данные и сообщения проверочного примера.
"""


class Product:
    def __init__(self, name, retail_price, purchase_price):
        self.name = name
        self.retail_price = retail_price
        self.purchase_price = purchase_price

    @property
    def profit(self):
        return self.retail_price - self.purchase_price

    @staticmethod
    def average_price(prices=None):
        if not prices:
            return 0
        return sum(prices) / len(prices)

    @property
    def information(self):
        return (
            f"название – {self.name}, розничная цена – {self.retail_price}, "
            f"закупочная цена – {self.purchase_price}"
        )


# Данные для проверки, не изменяйте их.
product_1 = Product("Картошка", 100, 90)
product_2 = Product("Перчатки", 150, 120)
product_3 = Product("Велосипед", 170, 150)

assortment_prices = [
    product_1.retail_price,
    product_2.retail_price,
    product_3.retail_price,
]

print(f"Средняя стоимость: {Product.average_price(assortment_prices)}")
print(f"Прибыль магазина с товара {product_1.name}: {product_1.profit}")
print(f"Информация о товаре {product_1.name}: {product_1.information}")

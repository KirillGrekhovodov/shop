from django.core.validators import MinValueValidator
from django.db import models


class Order(models.Model):
    name = models.CharField(max_length=50, verbose_name="Имя")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    address = models.CharField(max_length=50, verbose_name="Адрес")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    products = models.ManyToManyField(
        'webapp.Product',
        related_name="orders",
        through="webapp.OrderProduct",
        through_fields=("order", "product"),
    )

    class Meta:
        db_table = "orders"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderProduct(models.Model):
    qty = models.PositiveIntegerField(verbose_name="Количество", default=1, validators=(MinValueValidator(1),))
    product = models.ForeignKey("webapp.Product", on_delete=models.RESTRICT, verbose_name="Продукт")
    order = models.ForeignKey("webapp.Order", on_delete=models.RESTRICT, verbose_name="Заказ")

    class Meta:
        verbose_name = "Товар в заказа"
        verbose_name_plural = "Товары в заказе"

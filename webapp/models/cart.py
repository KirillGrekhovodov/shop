from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, F


class Cart(models.Model):
    qty = models.PositiveIntegerField(verbose_name="Количество", default=1, validators=(MinValueValidator(1),))
    product = models.ForeignKey("webapp.Product", on_delete=models.CASCADE, verbose_name="Продукт")

    def get_total_price(self):
        return self.qty * self.product.price

    @classmethod
    def get_full_total_price(cls):
        # return cls.objects.aggregate(total=Sum(F("qty") * F("product__price")))["total"]
        total = 0
        for cart in cls.objects.all():
            total += cart.get_total_price()
        return total

    class Meta:
        db_table = "cart"
        verbose_name = "Продукт в корзине"
        verbose_name_plural = "Продукты в корзине"

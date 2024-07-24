from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse


class Product(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")
    description = models.TextField(max_length=50, null=False, blank=False, verbose_name="Описание")
    amount = models.PositiveIntegerField(verbose_name="Остаток")
    price = models.DecimalField(verbose_name="Цена", max_digits=7, decimal_places=2, validators=(MinValueValidator(0),))
    category = models.ForeignKey("webapp.Category", on_delete=models.PROTECT, verbose_name="Категория")

    def __str__(self):
        return f"{self.pk} {self.title}"

    def get_absolute_url(self):
        return reverse("webapp:product_view", kwargs={"pk": self.pk})

    class Meta:
        db_table = "products"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

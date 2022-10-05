from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from webapp.forms import ProductForm
from webapp.models import Product, Order, OrderProduct


class TestOrdersMethods(TestCase):

    def setUp(self) -> None:
        print("setUp")

    def tearDown(self) -> None:
        pass

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData")
        cls.product = Product.objects.create(name="test", amount=3, price=50)
        cls.order = Order.objects.create(name="test", address="test", phone="test")

    def test_total_product_price(self):
        order_product = OrderProduct.objects.create(product=self.product, order=self.order, qty=2)
        self.assertEqual(order_product.get_sum(), 100)

    def test_order_total_price(self):
        product2 = Product.objects.create(name="test2", amount=5, price=30)
        OrderProduct.objects.create(product=self.product, order=self.order, qty=2)
        OrderProduct.objects.create(product=product2, order=self.order, qty=3)
        self.assertEqual(self.order.get_total(), 190)

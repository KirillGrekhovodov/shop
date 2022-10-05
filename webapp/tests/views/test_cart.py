from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from webapp.models import Product

User = get_user_model()


class TestAddDeleteCart(TestCase):

    def setUp(self) -> None:
        self.product = Product.objects.create(name="test", amount=3, price=50)
        admin, created = User.objects.get_or_create(username='admin')
        if created:
            admin.is_superuser = True
            admin.set_password('admin')
            admin.save()
        self.client.login(username='admin', password='admin')

    def test_add_cart(self):
        data = {"qty": 2}
        response = self.client.post(reverse("webapp:add_to_cart", kwargs={"pk": self.product.pk}), data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        session = self.client.session
        self.assertDictEqual(session.get("cart"), {str(self.product.pk): 2})

    def test_add_cart_qty_error(self):
        data = {"qty": 4}
        response = self.client.post(reverse("webapp:add_to_cart", kwargs={"pk": self.product.pk}), data=data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        session = self.client.session
        self.assertIsNone(session.get("cart"))

    def test_add_cart_existing_product(self):
        session = self.client.session
        session["cart"] = {self.product.pk: 1}
        session.save()
        data = {"qty": 1}
        response = self.client.post(reverse("webapp:add_to_cart", kwargs={"pk": self.product.pk}), data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        session = self.client.session
        cart = session.get("cart")
        self.assertEqual(len(cart), 1)
        self.assertDictEqual(cart, {str(self.product.pk): 2})

    def test_value_error(self):
        with self.assertRaises(ZeroDivisionError):
            2 / 0

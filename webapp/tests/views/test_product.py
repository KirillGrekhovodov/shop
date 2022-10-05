from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from webapp.models import Product


User = get_user_model()

class TestProduct(TestCase):

    def setUp(self) -> None:
        admin, created = User.objects.get_or_create(username='admin')
        if created:
            admin.is_superuser = True
            admin.set_password('admin')
            admin.save()
        self.client.login(username='admin', password='admin')

    def tearDown(self) -> None:
        pass

    @classmethod
    def setUpTestData(cls):
        pass

    def test_create_product(self):
        data = {'name': 'CreateTestProduct', 'price': 100, 'amount': 5, "category": 'food'}
        response = self.client.post(reverse("webapp:product_create"), data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        product = Product.objects.filter(name='CreateTestProduct')
        self.assertEqual(len(product), 1)
        self.assertEqual(product.first().price, 100)

    def test_create_product_not_category(self):
        data = {'name': 'CreateTestProduct', 'price': 100, 'amount': 5}
        response = self.client.post(reverse("webapp:product_create"), data=data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        product = Product.objects.filter(name='CreateTestProduct')
        self.assertEqual(len(product), 0)

    def test_update_product(self):
        pass

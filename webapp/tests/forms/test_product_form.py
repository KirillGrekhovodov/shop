from django.test import TestCase

from webapp.forms import ProductForm


class TestProductForm(TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @classmethod
    def setUpTestData(cls):
        pass

    def test_create_product_form(self):
        data = {'name': 'CreateTestProduct', 'price': 100, 'amount': 5, "category": 'food'}
        product_form = ProductForm(data=data)
        product_form.is_valid()
        self.assertEqual(product_form.cleaned_data.get("name"), "CreateTestProduct")

    def test_create_product_form_not_category(self):
        data = {'name': 'CreateTestProduct', 'price': 100, 'amount': 5}
        product_form = ProductForm(data=data)
        product_form.is_valid()
        self.assertEqual(product_form.errors.get("category")[0], "This field is required.")
        self.assertFalse(product_form.is_valid())

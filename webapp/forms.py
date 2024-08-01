from django import forms

from webapp.models import Product, Order


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Найти")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class CartForm(forms.Form):
    qty = forms.IntegerField(min_value=1)


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = ["name", "phone", "address"]

    def clean(self):
        data = super().clean()
        cart = self.request.session.get('cart', {})
        for product_id, qty in cart.items():
            try:
                product = Product.objects.get(pk=product_id)
                if qty > product.amount:
                    raise forms.ValidationError(f"Товар {product.title} закончился")
            except Product.DoesNotExist:
                raise forms.ValidationError(f"Один из товаров удален")
        return data

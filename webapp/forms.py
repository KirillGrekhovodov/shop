from django import forms

from webapp.models import Product, Cart, Order


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Найти")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["qty"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "phone", "address"]

    def clean(self):
        data = super().clean()
        for item in Cart.objects.all():
            if item.qty > item.product.amount:
                raise forms.ValidationError(f"Товар {item.product.title} закончился")
        return data

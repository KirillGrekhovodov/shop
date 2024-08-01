from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from webapp.forms import OrderForm
from webapp.models import Order, OrderProduct, Product


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("webapp:index")

    def form_invalid(self, form):
        return HttpResponseBadRequest(form.errors['__all__'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        with transaction.atomic():
            if self.request.user.is_authenticated:
                form.instance.user = self.request.user
            order = form.save()

            cart = self.request.session.get("cart", {})

            products = []
            orders_products = []

            for product_id, qty in cart.items():
                product = get_object_or_404(Product, id=product_id)
                orders_products.append(OrderProduct(order=order, product=product, qty=qty))
                product.amount -= qty
                products.append(product)

            OrderProduct.objects.bulk_create(orders_products)
            Product.objects.bulk_update(products, ("amount",))
            self.request.session.pop("cart")

        return HttpResponseRedirect(self.success_url)

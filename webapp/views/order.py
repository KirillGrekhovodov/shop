from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse_lazy
from django.views.generic import CreateView

from webapp.forms import OrderForm
from webapp.models import Order, Cart, OrderProduct, Product


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("webapp:index")

    # def form_valid(self, form):
    #
    #     with transaction.atomic():
    #         order = form.save()
    #         for item in Cart.objects.all():
    #             OrderProduct.objects.create(order=order, product=item.product, qty=item.qty)
    #             item.product.amount -= item.qty
    #             item.product.save()
    #             item.delete()
    #
    #     return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        return HttpResponseBadRequest(form.errors['__all__'])

    def form_valid(self, form):
        with transaction.atomic():
            order = form.save()
            products = []
            orders_products = []

            for item in Cart.objects.all():
                orders_products.append(OrderProduct(order=order, product=item.product, qty=item.qty))
                item.product.amount -= item.qty
                products.append(item.product)

            OrderProduct.objects.bulk_create(orders_products)
            Product.objects.bulk_update(products, ("amount",))
            Cart.objects.all().delete()

        return HttpResponseRedirect(self.success_url)

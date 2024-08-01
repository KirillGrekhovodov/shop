from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, TemplateView

from webapp.forms import CartForm, OrderForm
from webapp.models import Product


class CartAddView(View):
    def post(self, request, *args, **kwargs):
        # self.request.session['cart'] = {"1": 2, "2": 3, "3": 4, "4": 5}
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        form = CartForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['qty']
        else:
            return HttpResponseBadRequest(f"Некорректное значение")

        cart = self.request.session.get('cart', {})

        if str(product.pk) in cart:
            full_qty = cart[str(product.pk)] + qty
        else:
            full_qty = qty

        if full_qty > product.amount:
            return HttpResponseBadRequest(f"Количество товара {product.title} на складе всего {product.amount} щтук")

        if str(product.pk) not in cart:
            cart[str(product.pk)] = qty
        else:
            cart[str(product.pk)] += qty

        self.request.session['cart'] = cart
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse("webapp:index")


class CartView(TemplateView):
    template_name = "cart/cart_view.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        cart = self.request.session.get("cart", {})

        total = 0
        cart_list = []
        for product_id, qty in cart.items():
            product = get_object_or_404(Product, pk=product_id)
            total_price = product.price * qty
            cart_data = {
                "qty": qty,
                "product": product,
                "total_price": total_price
            }
            cart_list.append(cart_data)
            total += total_price

        context = super().get_context_data(object_list=None, **kwargs)
        context["total"] = total
        context["cart_list"] = cart_list
        context["form"] = OrderForm()
        return context


class CartDeleteView(View):

    def get(self, request, *args, pk, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        cart = self.request.session.get("cart", {})
        if str(product.pk) in cart:
            cart.pop(str(product.pk))
        self.request.session['cart'] = cart
        return redirect("webapp:cart")


class CartDeletePieceByPieceView(View):

    def post(self, request, *args, pk, **kwargs):
        form = CartForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['qty']
        else:
            return HttpResponseBadRequest(f"Некорректное значение")

        product = get_object_or_404(Product, pk=pk)
        cart = self.request.session.get("cart", {})
        if str(product.pk) in cart:
            cart[str(product.pk)] -= qty
        if cart[str(product.pk)] < 1:
            cart.pop(str(product.pk))
        self.request.session['cart'] = cart
        return redirect("webapp:cart")

from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from webapp.forms import CartForm, OrderForm
from webapp.models import Cart, Product


class CartAddView(CreateView):
    model = Cart
    form_class = CartForm

    def form_invalid(self, form):
        return HttpResponseBadRequest(f"Некорректное значение")

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        qty = form.cleaned_data['qty']

        try:
            cart = Cart.objects.get(product=product)
            full_qty = cart.qty + qty
        except Cart.DoesNotExist:
            full_qty = qty

        if full_qty > product.amount:
            return HttpResponseBadRequest(f"Количество товара {product.title} на складе всего {product.amount} щтук")

        cart_product, is_created = Cart.objects.get_or_create(product=product)
        if is_created:
            cart_product.qty = qty
        else:
            cart_product.qty += qty
        cart_product.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse("webapp:index")


class CartView(ListView):
    model = Cart
    context_object_name = "cart_list"
    template_name = "cart/cart_view.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context["total"] = Cart.get_full_total_price()
        context["form"] = OrderForm()
        return context


class CartDeleteView(DeleteView):
    model = Cart
    success_url = reverse_lazy("webapp:cart")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CartDeletePieceByPieceView(DeleteView):
    model = Cart
    form_class = CartForm

    def form_invalid(self, form):
        return HttpResponseBadRequest(f"Некорректное значение")

    def form_valid(self, form):
        qty = form.cleaned_data['qty']
        self.object.qty -= qty
        if self.object.qty < 1:
            self.object.delete()
        else:
            self.object.save()
        return redirect("webapp:cart")

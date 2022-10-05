from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, DeleteView, DetailView, CreateView

from webapp.forms import ProductForm
from webapp.models import Product
from webapp.views.base_view import SearchView


class IndexView(SearchView):
    model = Product
    template_name = 'product/index.html'
    ordering = ['category', 'name']
    search_fields = ['name__icontains']
    paginate_by = 6
    context_object_name = 'products'

    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)


class ProductView(DetailView):
    model = Product
    template_name = 'product/product_view.html'
    queryset = Product.objects.filter(amount__gt=0)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_create.html'

    def render_to_response(self, context, **response_kwargs):
        if context.get("form").errors:
            response_kwargs["status"] = HTTPStatus.BAD_REQUEST
        return super().render_to_response(context, **response_kwargs)

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk})


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_update.html'

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/product_delete.html'
    success_url = reverse_lazy('webapp:index')

from django.urls import path

from webapp.views import ProductListView, ProductCreateView, ProductDeleteView, ProductDetailView, ProductUpdateView

app_name = "webapp"

urlpatterns = [
    path('', ProductListView.as_view(), name="index"),
    path('articles/add/', ProductCreateView.as_view(), name="product_add"),
    path('article/<int:pk>/', ProductDetailView.as_view(), name="product_view"),
    path('article/<int:pk>/update/', ProductUpdateView.as_view(), name="product_update"),
    path('article/<int:pk>/delete/', ProductDeleteView.as_view(), name="product_delete"),
]
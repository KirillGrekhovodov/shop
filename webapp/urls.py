from django.urls import path

from webapp.views import ProductListView, ProductCreateView, ProductDeleteView, ProductDetailView, ProductUpdateView, \
    CartAddView, CartView, CartDeleteView, CartDeletePieceByPieceView, OrderCreateView

app_name = "webapp"

urlpatterns = [
    path('', ProductListView.as_view(), name="index"),
    path('products/add/', ProductCreateView.as_view(), name="product_add"),
    path('product/<int:pk>/', ProductDetailView.as_view(), name="product_view"),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name="product_update"),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name="product_delete"),
    path('product/<int:pk>/add-cart/', CartAddView.as_view(), name="product_add_cart"),
    path('cart/', CartView.as_view(), name="cart"),
    path('cart/<int:pk>/remove/', CartDeleteView.as_view(), name="delete_from_cart"),
    path(
        'cart/<int:pk>/remove-piece-by-piece/',
        CartDeletePieceByPieceView.as_view(),
        name="delete_from_cart_piece_by_piece"
    ),
    path('order/create/', OrderCreateView.as_view(), name="order_create"),
]

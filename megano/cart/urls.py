from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:product_seller_id>/", views.cart_add, name="cart_add"),
    path("remove/<int:product_seller_id>/", views.remove_cart, name="remove_cart"),
    path(
        "add_inside_cart/<int:product_seller_id>",
        views.add_inside_cart,
        name="add_inside_cart",
    ),
    path(
        "remove_inside_cart/<int:product_seller_id>",
        views.remove_inside_cart,
        name="remove_inside_cart",
    ),
]

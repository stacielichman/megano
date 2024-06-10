from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    AccountDetailView,
    CatalogView,
    CompareManager,
    DiscountDetailView,
    DiscountListView,
    HistoryOrder,
    LastOrderDetailView,
    MainPageView,
    OrderDetailView,
    ProductDetailView,
    ProfileUpdateView,
    SellerDetailView,
    set_language,
)

app_name = "shopapp"

urlpatterns = [
    path("", MainPageView.as_view(), name="index"),
    path("about/<int:pk>/", SellerDetailView.as_view(), name="seller_detail"),
    path("discounts/", DiscountListView.as_view(), name="discounts"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product"),
    path("comparison/", CompareManager.as_view(), name="compare"),
    path("discounts/<int:pk>/", DiscountDetailView.as_view(), name="discount_details"),
    path("profile/details/<int:pk>/", AccountDetailView.as_view(), name="profile"),
    path("profile/details/update/", ProfileUpdateView.as_view(), name="profile_update"),
    path("profile/order/history/", HistoryOrder.as_view(), name="history_order"),
    path(
        "profile/order/history/<int:pk>/",
        OrderDetailView.as_view(),
        name="order_details",
    ),
    path(
        "profile/<int:pk>/order/last/",
        LastOrderDetailView.as_view(),
        name="last_order_details",
    ),
    path(
        "categories/products/sorted-products/<int:pk>",
        CatalogView.as_view(),
        name="catalog",
    ),
]

urlpatterns += [
    path(r"set-language/", set_language, name="set_language"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

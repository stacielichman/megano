from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path("auth/", include("user.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    path("cart/", include("cart.urls")),
    path("pay/", include("pay.urls")),
    path(
        "",
        include(
            "shopapp.urls",
        ),
    ),
)
if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

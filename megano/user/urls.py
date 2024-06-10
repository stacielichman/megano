from django.urls import path

from .views import (
    Login,
    Reset_Password,
    Reset_Password_Complete,
    Reset_Password_Confirm,
    Reset_Password_Done,
    logout_view,
    register,
)

app_name = "auth"

urlpatterns = [
    path("", Login.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register, name="register"),
    path("recovery/e-mail/", Reset_Password.as_view(), name="recovery_password"),
    path(
        "recovery/e-mail/done/",
        Reset_Password_Done.as_view(),
        name="password_reset_done",
    ),
    path(
        "recovery/e-mail/confirm/<uidb64>/<token>/",
        Reset_Password_Confirm.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "recovery/e-mail/complete/",
        Reset_Password_Complete.as_view(),
        name="password_reset_complete",
    ),
]

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PayConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pay"
    verbose_name = _("pay")

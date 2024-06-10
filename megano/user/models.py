from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    class Meta:
        verbose_name = _("роль")
        verbose_name_plural = _("Роли")

    name = models.CharField(max_length=50, unique=True, verbose_name=_("имя"))

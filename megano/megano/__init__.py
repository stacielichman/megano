from __future__ import absolute_import, unicode_literals

from megano.settings import ON_PAYMENT

if ON_PAYMENT:
    from .celery import app as celery_app

    __all__ = ("celery_app",)

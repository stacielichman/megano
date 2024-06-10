import os

from megano.settings import ON_PAYMENT

if ON_PAYMENT:
    from celery import Celery

    app = Celery("payment")
    app.config_from_object("django.conf.settings", namespace="CELERY")
    app.autodiscover_tasks()

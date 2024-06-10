from django.urls import path

from .views import (
    order_step_1,
    order_step_2,
    order_step_3,
    order_step_4,
    payment_card,
    payment_invoice,
    proof_payment,
)

app_name = "pay"

urlpatterns = [
    path("step_1/", order_step_1, name="step_1"),
    path("step_2/", order_step_2, name="step_2"),
    path("step_3/<int:id>/", order_step_3, name="step_3"),
    path("step_4/<int:id>/", order_step_4, name="step_4"),
    path("payment/<int:id>/", payment_card, name="payment"),
    path("paymentsomeone/<int:id>/", payment_invoice, name="paymentsomeone"),
    path("progressPayment/", proof_payment, name="progressPayment"),
]

from megano.celery import app
from pay.models import Transaction


@app.task
def process_payment(pk):
    transaction = Transaction.objects.get(pk)
    if transaction.uuid // 2 == 0 and len(transaction.uuid) == 8:
        transaction.payment_status = "paid"
        transaction.order.payment_status = "paid"
        transaction.save()
        transaction.order.save()

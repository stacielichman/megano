from django.contrib import admin

from pay.models import Order, OrderItem, Transaction

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Transaction)

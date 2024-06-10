from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from cart.cart import Cart
from megano.settings import ON_PAYMENT
from shopapp.models import Profile

from .forms import DeliveryForm, PaymentForm, PaymentTypeForm, UserRegistrationForm
from .models import Order, OrderItem, Transaction


def order_step_1(request):
    context = {
        "form_user": UserRegistrationForm,
    }
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("pay:step_2")
        return render(request, "pay/order_step_1.html", context=context)
    elif request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            name = user_form.cleaned_data["username"]
            email = user_form.cleaned_data["email"]
            password = user_form.cleaned_data["password"]
            phone = user_form.cleaned_data["phone"]
            user = User.objects.create_user(
                username=email, first_name=name, email=email, password=password
            )
            user.save()
            profile = Profile.objects.create(user=user, phone=phone)
            profile.save()

            new_user = authenticate(request=request, username=email, password=password)
            if new_user:
                login(request, new_user)
                return redirect("pay:step_2")


def order_step_2(request):
    context = {
        "form_order": DeliveryForm,
    }
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("pay:step_1")
        return render(request, "pay/order_step_2.html", context=context)
    elif request.method == "POST":
        order_form = DeliveryForm(request.POST)
        if order_form.is_valid():
            delivery = order_form.cleaned_data["delivery"]
            city = order_form.cleaned_data["city"]
            address = order_form.cleaned_data["address"]
            user = request.user
            order = Order(user=user, city=city, address=address, delivery=delivery)
            order.save()
            return redirect("pay:step_3", id=order.id)


def order_step_3(request, id):
    context = {
        "form_payment_type": PaymentTypeForm,
        "order_id": id,
    }
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("pay:step_1")
        return render(request, "pay/order_step_3.html", context=context)
    elif request.method == "POST":
        payment_form = PaymentTypeForm(request.POST)
        if payment_form.is_valid():
            payment_type = payment_form.cleaned_data["type"]
            order = Order.objects.get(pk=id)
            order.payment_type = payment_type
            order.save()
            return redirect("pay:step_4", id=id)


def order_step_4(request, id):
    cart = Cart(request)
    order = Order.objects.get(pk=id)
    context = {
        "order_id": id,
        "order": order,
        "cart": cart,
    }
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("pay:step_1")
        return render(request, "pay/order_step_4.html", context=context)
    elif request.method == "POST":
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product_seller"],
                price=item["price"],
                old_price=item["price"],
                count=item["quantity"],
            )
        amount = cart.get_total_price()
        transaction = Transaction(
            order_id=order.id,
            amount=amount,
            user=request.user,
        )
        transaction.save()
        cart.clear()
        if order.payment_type == "online":
            return redirect("pay:payment", id=transaction.id)
        else:
            return redirect("pay:paymentsomeone", id=transaction.id)


def payment_card(request, id):
    if request.method == "GET":
        form = PaymentForm()
        return render(request, "pay/payment_card.html", {"form": form})
    elif request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            uuid = form.data["card_number"]
            transaction = Transaction.objects.get(id=id)
            if ON_PAYMENT:
                from .tasks import process_payment

                process_payment.delay(transaction.id)
            transaction.uuid = uuid
            transaction.save()
        return redirect("pay:progressPayment")


def payment_invoice(request, id):
    if request.method == "GET":
        form = PaymentForm()
        return render(request, "pay/payment_invoice.html", {"form": form})
    elif request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            uuid = form.data["card_number"]
            transaction = Transaction.objects.get(id=id)
            if ON_PAYMENT:
                from .tasks import process_payment

                process_payment.delay(transaction.id)
            transaction.uuid = uuid
            transaction.save()
        return redirect("pay:progressPayment")


def proof_payment(request):
    return render(request, "pay/progress_payment.html")

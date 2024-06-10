from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from shopapp.models import Profile


class UserRegistrationForm(forms.Form):
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Confirm password"), widget=forms.PasswordInput)
    username = forms.CharField(label=_("Full name"), widget=forms.TextInput)
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput)
    phone = forms.CharField(
        label=_("Phone number"),
        empty_value="",
        widget=forms.TextInput,
    )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match")
        else:
            return cd["password2"]


class PaymentForm(forms.Form):
    card_number = forms.CharField(
        label=_("Card number"),
        max_length=9,
        widget=forms.TextInput(
            attrs={
                "class": "form-input Payment-bill",
                "placeholder": "9999 9999",
                "data-mask": "9999 9999",
                "data-validate": "require pay",
            }
        ),
    )


class DeliveryForm(forms.Form):
    delivery_options = [
        ("ordinary", _("Ordinary delivery")),
        ("express", _("Express delivery")),
    ]

    delivery = forms.ChoiceField(
        label=_("Delivery type"), choices=delivery_options, widget=forms.RadioSelect()
    )
    city = forms.CharField(
        label=_("City"), widget=forms.TextInput(attrs={"class": "form-input"})
    )
    address = forms.CharField(
        label=_("Address"), widget=forms.Textarea(attrs={"class": "form-textarea"})
    )


class PaymentTypeForm(forms.Form):
    payment_options = [
        ("online", _("Online by card")),
        ("someone", _("Online by randomly generated account")),
    ]

    type = forms.ChoiceField(
        label=_("Delivery type"), choices=payment_options, widget=forms.RadioSelect()
    )

from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=1,
        label="Количество",
        widget=forms.NumberInput(attrs={"class": "Amount-input form-input"}),
    )
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

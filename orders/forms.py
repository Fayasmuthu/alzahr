from django import forms

from .models import Order, WhatsAppOrder


class OrderForm(forms.ModelForm):
    selected_dial_code_mobile = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )
    selected_dial_code_alternative = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )

    class Meta:
        model = Order
        fields = [
            "full_name",
            "address_line_1",
            "address_line_2",
            "mobile_no",
            "alternative_no",
            "state",
            "district",
            "city",
            "pin_code",
            "email",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Full name"}
            ),
            "address_line_1": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "House/Floor No. Building Name or Street, Locality",
                }
            ),
            "address_line_2": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Any nearby post office, market, Hospital as the landmark",
                }
            ),
            "mobile_no": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Mobile No",
                    "type": "tel",
                    "maxlength": "10",
                }
            ),
            "alternative_no": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Alternative Mobile No",
                    "type": "tel",
                    "maxlength": "10",
                }
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "State"}
            ),
            "district": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "District"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
            "pin_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Pin Code"}
            ),
            "email": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Email", "type": "email"}
            ),
        }


class WhatsAppOrderForm(forms.ModelForm):
    class Meta:
        model = WhatsAppOrder
        # fields = ['product', 'quantity', 'customer_name', 'customer_phone']
        fields = ['product', 'quantity']

        widgets = {
            'product': forms.HiddenInput(),
        }
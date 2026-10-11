from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["cust_name", "address", "dob", "mob_no", "gender"]
        widgets = {
            "cust_name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "address": forms.Textarea(attrs={"rows": 3, "placeholder": "Customer address"}),
            "dob": forms.DateInput(attrs={"type": "date"}),
            "mob_no": forms.TextInput(attrs={"placeholder": "Mobile number"}),
        }

class MoneyForm(forms.Form):
    account_no = forms.CharField(max_length=16, label="Account number")
    amount = forms.DecimalField(min_value=0.01, max_digits=12, decimal_places=2)
    note = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={"placeholder": "Optional note"}))

class TransferForm(forms.Form):
    from_account = forms.CharField(max_length=16, label="From account")
    to_account = forms.CharField(max_length=16, label="To account")
    amount = forms.DecimalField(min_value=0.01, max_digits=12, decimal_places=2)
    note = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={"placeholder": "Optional note"}))

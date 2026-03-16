from django import forms
from .models import ImportOrderItem

class ImportOrderItemForm(forms.ModelForm):

    class Meta:
        model = ImportOrderItem
        fields = ['product','quantity','unit_price']
        widgets = {
            'product': forms.Select(attrs={"class": "form-select  fw-bold text-dark"}),


            "quantity": forms.NumberInput(attrs={
                "class": "form-control  fw-bold text-dark",
                "min": "1",
                "value": "1"
            }),
            "unit_price": forms.NumberInput(attrs={
                "class": "form-control  fw-bold text-dark",
                "min": "0"
            })
        }
from django import forms
from .models import ImportOrderItem


from warehouse.models import Warehouse
from productwarehouse.models import ProductWarehouse


class ImportOrderItemForm(forms.ModelForm):
    warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        required=True,
        label="Kho nhập"
    )

    class Meta:
        model = ImportOrderItem
        fields = ['product','quantity','unit_price','warehouse']
        widgets = {
            'product': forms.Select(attrs={"class": "form-select fw-bold text-dark"}),


            "quantity": forms.NumberInput(attrs={
                "class": "form-control  fw-bold text-dark",
                "min": "1",
                "value": "1"
            }),
            "unit_price": forms.NumberInput(attrs={
                "class": "form-control  fw-bold text-dark",
                "min": "0"
            }),
            'warehouse': forms.Select(attrs={"class": "form-select fw-bold text-dark"}),
        }
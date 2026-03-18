from django import forms
from .models import ExportOrderItem



class ExportOrderItemForm(forms.ModelForm):
    class Meta:

        model = ExportOrderItem
        fields = ['product', 'quantity', 'unit_price']
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

        def clean(self):
            cleaned_data = super().clean()

            product = cleaned_data.get('product')
            quantity = cleaned_data.get('quantity')

            if product and quantity:
                if product.quantity_in_stock < quantity:
                    raise forms.ValidationError(
                        f"Sản phẩm {product.name} không đủ tồn kho"
                    )

            return cleaned_data
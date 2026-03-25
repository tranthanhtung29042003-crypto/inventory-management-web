from django import forms
from .models import ExportOrderItem
from productwarehouse.models import ProductWarehouse


class ExportOrderItemForm(forms.ModelForm):

    class Meta:
        model = ExportOrderItem
        fields = ['product', 'quantity', 'unit_price', 'warehouse']

        widgets = {
            'product': forms.Select(attrs={"class": "form-select fw-bold text-dark"}),

            "quantity": forms.NumberInput(attrs={
                "class": "form-control fw-bold text-dark",
                "min": "1",
                "value": "1"
            }),

            "unit_price": forms.NumberInput(attrs={
                "class": "form-control fw-bold text-dark",
                "min": "0"
            }),

            "warehouse": forms.Select(attrs={
                "class": "form-select fw-bold text-dark"
            })
        }

    def clean(self):
        cleaned_data = super().clean()

        warehouse = cleaned_data.get('warehouse')  # ✅ FIX
        quantity = cleaned_data.get('quantity')

        # ✅ auto sync product từ ProductWarehouse
        if warehouse:
            cleaned_data['product'] = warehouse.product

        # ✅ check tồn kho trực tiếp
        if warehouse and quantity:
            stock = warehouse.quantity

            if quantity > stock:
                raise forms.ValidationError(
                    f"{warehouse.product.name} chỉ còn {stock} trong kho"
                )

        return cleaned_data
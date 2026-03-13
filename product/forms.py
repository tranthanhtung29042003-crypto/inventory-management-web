from django import forms
from product.models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "import_price": forms.NumberInput(attrs={"class": "form-control"}),
            "sell_price": forms.NumberInput(attrs={"class": "form-control"}),
            "quantity_in_stock": forms.NumberInput(attrs={"class": "form-control"}),
            "min_stock_level": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()

        import_price = cleaned_data.get("import_price")
        sell_price = cleaned_data.get("sell_price")

        if import_price and sell_price:
            if sell_price < import_price:
                raise forms.ValidationError(
                    "Sell price must be greater than import price"
                )

        return cleaned_data
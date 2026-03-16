from django import forms
from django.forms import modelformset_factory

from .models import ImportOrder
from importorderitem.forms import ImportOrderItemForm
from importorderitem.models import ImportOrderItem

from .services.generate_importoder_code import generate_importoder_code


class ImportOrderForm(forms.ModelForm):

    class Meta:
        model = ImportOrder
        fields = ['code', 'supplier', 'invoice_file']
        widgets = {
            "supplier": forms.Select(attrs={"class": "form-select text-dark"}),
            "invoice_file": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # hiển thị code auto
        self.fields['code'].initial = self.instance.code or generate_importoder_code()

        # không cho sửa
        self.fields['code'].disabled = True


ImportOrderItemFormSet = modelformset_factory(
    ImportOrderItem,
    form=ImportOrderItemForm,
    extra=1,
    can_delete=True
)
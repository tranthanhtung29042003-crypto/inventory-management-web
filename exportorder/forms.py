from django import forms
from django.forms import modelformset_factory

from .models import ExportOrder
from exportorderitem.forms import ExportOrderItemForm
from exportorderitem.models import ExportOrderItem

from .services.generate_importoder_code import generate_exportoder_code



class ExportOrderForm(forms.ModelForm):

    class Meta:
        model = ExportOrder
        fields = ['code', 'customer_name', 'note']
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": "form-control"}),
            "note": forms.Textarea(attrs={"class": "form-control"}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # hiển thị code auto
        self.fields['code'].initial = self.instance.code or generate_exportoder_code()

        # không cho sửa
        self.fields['code'].disabled = True


ExportOrderItemFormSet = modelformset_factory(
    ExportOrderItem,
    form=  ExportOrderItemForm,
    extra=1,
    can_delete=True
)
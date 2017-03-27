from django import forms
from .models import Variations
from django.forms.models import modelformset_factory


class VariationInventoryForm(forms.ModelForm):
    class Meta:
        model = Variations
        fields = [
            "price",
            "sale_price",
            "inventory"
        ]

VariationInventoryFormSet = modelformset_factory(Variations, form=VariationInventoryForm, extra=2)
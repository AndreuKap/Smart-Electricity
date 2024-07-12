from django import forms
from .models import Cost

class CostFormEN(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ['cost_dey', 'cost_night']


class CostFormUA(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ['cost_dey', 'cost_night']
        labels = {
            'cost_dey': 'дений тариф',
            'cost_night': 'Нічний тариф',
        }
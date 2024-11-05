from django import forms
from .models import Record

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = [
            'caller_name',
            'caller_phone',
            'caller_zip_code', 
            'caller_neighborhood',
            'caller_street',
            'caller_house_number', 
            'is_caller_part_of',
            'is_caller_wating',
            'fact_date'
        ]

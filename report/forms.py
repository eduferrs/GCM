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
            'fact_date',
            'call_date',

            'incident_zip_code',
            'incident_neighborhood',
            'incident_street',
            'incident_house_number',
            'reference_point',
            'suspect_skin_color',
            'suspect_haircut_style',
            'suspect_tatoos',
            'suspect_approximate_age',
            'suspect_approximate_height',
            'suspect_description',
            'nature_of_the_incident',
            'is_there_a_firearm',
            'child_involved',
            'number_of_people_involved',
            'type_of_incident',

            'vehicle',
            'vehicle_model',
            'vehicle_color',
            'vehicle_type',
            'are_there_victims',
            'ambulance_required',
            'priority_incident',

            'is_dispatched',
            'is_finished',

            'incident_dispatch_VTR',
            'response_team',
            'dispatched_by',

        ]
    call_date = forms.DateTimeField(required=False)

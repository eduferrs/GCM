import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from report.models import IncidentType 

def populate_incident_types():
    tipos_de_incidentes = [
        'Acidente de trânsito', 'Violência doméstica', 'Maus-tratos de criança',
        'Maus-tratos de animais', 'Morador de rua', 'Poluição sonora', 'Invasão',
        'Desmatamento', 'Desinteligência', 'Ocorrência em escola', 'Próprios públicos',
        'Furto de fios', 'Comércio irregular', 'Pipa com linha cortante', 'Fogueira', 'Incêndio'
    ]
    
    for tipo in tipos_de_incidentes:
        IncidentType.objects.get_or_create(type=tipo)

populate_incident_types()

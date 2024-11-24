from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


#Atributos do User padrão (já vem criado com o Django). 

#username: Único. Pode ser utilizado para login.
#first_name: Opcional.
#last_name: Opcional.
#email: Opcional, mas pode ser configurado como obrigatório e usado para login.
#password: Armazenada com criptografia.
#is_staff: Boolean para indicar se o usuário pode acessar o painel de administrador.
#is_active: Boolean. Usuários inativos não podem fazer login.
#is_superuser: Boolean para indicar usuários que possuem todas as permissões.
#last_login: Armazena data e hora do ultimo login.
#date_joined: Armazena data e hora do cadastro.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    re = models.CharField(unique=True, max_length=12)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - RE: {self.re}"


class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_records')
    caller_name = models.CharField(max_length=100, blank=True, default="Não Informado") 
    caller_phone = models.CharField(max_length=15, blank=True, default="Não Informado")
    caller_zip_code = models.CharField(max_length=13, blank=True, default="Não Informado")
    caller_neighborhood = models.CharField(max_length=100, blank=True, default="Não Informado")
    caller_street = models.CharField(max_length=100, blank=True, default="Não Informado")
    caller_house_number = models.CharField(max_length=13, blank=True, default="Não Informado")
    is_caller_part_of = models.BooleanField(default=False)
    is_caller_wating = models.BooleanField(default=False)
    fact_date = models.DateTimeField(null=True)
    call_date = models.DateTimeField(null=True)

    incident_zip_code = models.CharField(max_length=9)
    incident_neighborhood = models.CharField(max_length=100)
    incident_street = models.CharField(max_length=100)
    incident_house_number = models.CharField(max_length=5)
    reference_point = models.CharField(max_length=100, blank=True, default="Não Informado")
    suspect_skin_color = models.CharField(max_length=15, blank=True, default="Não Informado")
    suspect_haircut_style = models.CharField(max_length=15, blank=True, default="Não Informado")
    suspect_tatoos = models.CharField(max_length=254, blank=True, default="Não Informado")
    suspect_approximate_age = models.CharField(max_length=15, blank=True, default="Não Informado")
    suspect_approximate_height = models.CharField(max_length=15, blank=True, default="Não Informado")
    suspect_description = models.CharField(max_length=254, blank=True, default="Não Informado")

    nature_of_the_incident = models.CharField(max_length=100)
    is_there_a_firearm = models.BooleanField(default=False)
    child_involved = models.BooleanField(default=False)
    number_of_people_involved = models.CharField(max_length=15, blank=True, default="Não Informado")
    type_of_incident = models.CharField(max_length=100)

    vehicle = models.CharField(max_length=100, blank=True, default="Não se aplica")
    vehicle_model = models.CharField(max_length=100, blank=True, default="Não se aplica")
    vehicle_color = models.CharField(max_length=100, blank=True, default="Não se aplica")
    vehicle_type = models.CharField(max_length=100, blank=True, default="Não se aplica")
    are_there_victims = models.BooleanField(default=False)
    ambulance_required = models.BooleanField(default=False)
    priority_incident = models.BooleanField(default=False)
    is_dispatched = models.BooleanField(default=False)
    

    incident_dispatch_VTR = models.CharField(max_length=100, blank=True)
    response_team = models.CharField(max_length=100, blank=True)
    dispatched_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='dispatched_records', null=True, blank=True)
    dispatch_date = models.DateTimeField(null=True)

    ro = models.BooleanField(default=False)
    ri = models.BooleanField(default=False)
    joint_operation = models.BooleanField(default=False)
    police_district = models.CharField(max_length=100, blank=True, default="Não Informado")
    bopc = models.CharField(max_length=100, blank=True, default="Não Informado")
    police_chief_qra = models.CharField(max_length=100, blank=True, default="Não Informado")
    incident_conclusion_time = models.DateTimeField(null=True)
    officer_in_charge = models.CharField(max_length=100, blank=True)
    notification_time = models.DateTimeField(null=True)
    officer_in_charge_actions = models.CharField(max_length=254, blank=True)
    is_finished = models.BooleanField(default=False)
    finished_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='finished_records', null=True, blank=True)


    def __str__(self):
        return f"{self.id} - { self.caller_name } - {self.type_of_incident}"




class IncidentType(models.Model):
    type = models.CharField(max_length=254)

    def __str__(self):
        return f"{self.type}"
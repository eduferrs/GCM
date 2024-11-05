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
    user = models.ForeignKey(User, on_delete=models.PROTECT)
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

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


#Atributos do User padrão (já vem criado com o Django). 
##Atualmente apenas username e password estão sendo utilizados para o cadastro.
###is_active é definido como True automaticamente ao realizar um cadastro.

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


# Create your models here.
class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    ne = models.IntegerField(unique=True, validators=[MaxValueValidator(99999999999)])
    caller_name = models.CharField(max_length=100, blank=True, default="Não Informado") 
    caller_phone = models.CharField(max_length=15, blank=True, default="Não Informado")
    caller_address = models.CharField(max_length=150, blank=True)
    is_caller_part_of = models.BooleanField(default=False)
    is_caller_wating = models.BooleanField(default=False)
    fact_date = models.DateTimeField(null=True)
    call_date = models.DateTimeField(null=True)

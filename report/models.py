from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator



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

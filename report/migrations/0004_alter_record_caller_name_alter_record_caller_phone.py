# Generated by Django 5.1.2 on 2024-10-29 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_alter_record_caller_name_alter_record_caller_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='caller_name',
            field=models.CharField(default='Não Informado', max_length=100),
        ),
        migrations.AlterField(
            model_name='record',
            name='caller_phone',
            field=models.CharField(default='Não Informado', max_length=15),
        ),
    ]

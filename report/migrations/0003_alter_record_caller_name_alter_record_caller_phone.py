# Generated by Django 5.1.2 on 2024-10-29 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_alter_record_call_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='caller_name',
            field=models.CharField(blank=True, default='Não Informado', max_length=100),
        ),
        migrations.AlterField(
            model_name='record',
            name='caller_phone',
            field=models.CharField(blank=True, default='Não Informado', max_length=15),
        ),
    ]

# Generated by Django 5.1.2 on 2024-11-05 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0006_remove_record_caller_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='caller_house_number',
            field=models.CharField(blank=True, default='Não Informado', max_length=13),
        ),
        migrations.AlterField(
            model_name='record',
            name='caller_zip_code',
            field=models.CharField(blank=True, default='Não Informado', max_length=13),
        ),
    ]

# Generated by Django 5.1.2 on 2024-11-07 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0008_incidenttype_record_ambulance_required_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='incident_street',
            field=models.CharField(default='a', max_length=100),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.1.2 on 2024-10-28 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='call_date',
            field=models.DateTimeField(null=True),
        ),
    ]

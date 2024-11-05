# Generated by Django 5.1.2 on 2024-11-04 23:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0004_alter_record_caller_name_alter_record_caller_phone'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='ne',
        ),
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
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('re', models.CharField(max_length=12, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

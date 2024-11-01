# Generated by Django 5.1.2 on 2024-10-28 04:04

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ne', models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(99999999999)])),
                ('caller_name', models.CharField(blank=True, max_length=100)),
                ('caller_phone', models.CharField(blank=True, max_length=15)),
                ('caller_address', models.CharField(blank=True, max_length=150)),
                ('is_caller_part_of', models.BooleanField(default=False)),
                ('is_caller_wating', models.BooleanField(default=False)),
                ('fact_date', models.DateTimeField(null=True)),
                ('call_date', models.DateField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0003_auto_20171026_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='emergency_type',
            field=models.CharField(choices=[('HR', 'Harassment'), ('BG', 'Burglary'), ('RB', 'Robbery'), ('TH', 'Theft'), ('AR', 'Arson'), ('AS', 'Assault'), ('MD', 'Murder'), ('OT', 'Other')], default='OT', max_length=2),
        ),
    ]

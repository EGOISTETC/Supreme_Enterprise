# Generated by Django 5.0.4 on 2024-04-26 21:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyticapi', '0004_analytics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='Referal_Url',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='analyticapi.referal'),
        ),
    ]

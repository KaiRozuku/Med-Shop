# Generated by Django 4.2.11 on 2024-05-16 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_drug_is_booked_drug_about_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
    ]

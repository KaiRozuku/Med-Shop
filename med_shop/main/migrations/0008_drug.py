# Generated by Django 4.2.11 on 2024-05-16 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_delete_drug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('developer', models.CharField(max_length=70)),
                ('appointment', models.CharField(max_length=70)),
                ('measurement', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='')),
                ('price', models.FloatField(default=0.0)),
                ('about_product', models.TextField(blank=True)),
                ('indication', models.TextField(blank=True)),
                ('contraindication', models.TextField(blank=True)),
                ('dose', models.TextField(blank=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.category')),
            ],
        ),
    ]

# Generated by Django 4.2.11 on 2024-05-24 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='main/img/149071.png', upload_to='profile_pictures/'),
        ),
    ]

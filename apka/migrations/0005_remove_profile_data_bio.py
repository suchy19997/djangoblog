# Generated by Django 4.1.5 on 2023-02-05 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apka', '0004_profile_data_delete_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile_data',
            name='bio',
        ),
    ]
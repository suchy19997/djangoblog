# Generated by Django 4.1.5 on 2023-02-04 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apka', '0002_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
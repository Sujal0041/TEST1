# Generated by Django 4.2.7 on 2024-05-26 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sujal", "0002_customuser_name_customuser_phone"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="name",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="phone",
        ),
    ]

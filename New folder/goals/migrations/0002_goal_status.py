# Generated by Django 4.2.7 on 2024-04-21 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("goals", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="goal",
            name="status",
            field=models.CharField(default="Ongoing", max_length=255),
            preserve_default=False,
        ),
    ]
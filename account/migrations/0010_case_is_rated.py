# Generated by Django 4.2.10 on 2024-03-13 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_case_is_running'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='is_rated',
            field=models.BooleanField(default=False),
        ),
    ]

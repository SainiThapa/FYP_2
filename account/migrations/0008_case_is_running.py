# Generated by Django 4.2.10 on 2024-03-11 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_case_case_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='is_running',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 4.2.10 on 2024-03-09 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_connection_case'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='case_title',
            field=models.CharField(default='New Case', max_length=60),
        ),
    ]
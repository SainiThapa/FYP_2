# Generated by Django 4.2.10 on 2024-03-06 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_client_id_alter_lawyer_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='id',
        ),
        migrations.RemoveField(
            model_name='lawyer',
            name='id',
        ),
    ]

# Generated by Django 4.2.10 on 2024-03-16 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_alter_lawyer_ratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='case_title',
            field=models.CharField(default='New Case', max_length=128),
        ),
    ]
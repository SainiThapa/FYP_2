# Generated by Django 4.2.10 on 2024-03-06 16:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_lawyer_specialization_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='lawyer',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='academic_degree',
            field=models.ImageField(blank=True, null=True, upload_to='academic_degree/'),
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='license_img',
            field=models.ImageField(null=True, upload_to='license_img/'),
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='lawyer_profile_picture/'),
        ),
    ]

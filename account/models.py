import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
User = get_user_model()


# class User(AbstractBaseUser):
#     USERNAME_FIELD="username"

class Client(models.Model):
    # is_active=models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username=models.CharField(max_length=128,unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=128,null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    location = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)

    def __str__(self):
        return self.username


class Lawyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_picture', null=True, blank=True)
    location = models.CharField(max_length=255)
    specialization_tags = models.JSONField(default=list)
    profile_description = models.TextField()
    license_no = models.PositiveIntegerField(null=True)
    license_img = models.ImageField(upload_to='license_img', null=True, blank=False)
    license_location = models.CharField(max_length=255, null=True)
    license_verify_status = models.BooleanField(default=False)
    academic_degree = models.ImageField(upload_to='academic_degree', null=True, blank=True)
    completion_year = models.PositiveIntegerField(null=True)
    major_subject = models.CharField(max_length=255, null=True)


class File(models.Model):
    file_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_description=models.TextField()
    client=models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.client.name} - {self.file_id} - {self.file_description}"
    

class CASE(models.Model):
    VICTORY = 'VICTORY'
    DEFEAT = 'DEFEAT'
    STATUS_CHOICES = [
        (VICTORY, 'Victory'),
        (DEFEAT, 'Defeat'),
    ]
    file=models.ForeignKey(File,on_delete=models.CASCADE)
    lawyer=models.ForeignKey(Lawyer,on_delete=models.CASCADE)
    ratings = models.DecimalField(max_digits=2, decimal_places=1, default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])  # noqa: F821
    case_status=models.CharField(max_length=7, choices=STATUS_CHOICES, default=VICTORY)
    case_approval=models.BooleanField(default=False)
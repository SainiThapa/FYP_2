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
    username=models.CharField(max_length=128)
    email=models.EmailField()
    password=models.CharField(max_length=128,null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    location = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)

    def __str__(self):
        return self.username


class Lawyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=255)
    password=models.CharField(max_length=128)
    email=models.EmailField(max_length=128)
    profile_picture = models.ImageField(upload_to='lawyer_profile_picture/', null=True, blank=True)
    location = models.CharField(max_length=255)
    phone=models.BigIntegerField(null=True)
    specialization_tags = models.TextField()
    profile_description = models.TextField()
    ratings = models.DecimalField(max_digits=2, decimal_places=1, default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    license_no = models.PositiveIntegerField(null=True)
    license_img = models.ImageField(upload_to='license_img/', null=True, blank=False)
    license_location = models.CharField(max_length=255, null=True)
    license_verify_status = models.BooleanField(default=False)
    academic_degree = models.ImageField(upload_to='academic_degree/', null=True, blank=True)
    completion_year = models.DateField(null=True)
    major_subject = models.CharField(max_length=255, null=True)
    
    def __str__(self):
            return self.username
    
    def save(self, *args, **kwargs):
        user = User.objects.get(email=self.email)

        if self.license_verify_status:
            user.is_active = True
            user.save()
        super().save(*args, **kwargs)


class File(models.Model):
    file_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_title=models.CharField(max_length=128)
    file_description=models.TextField()
    client=models.ForeignKey(Client, on_delete=models.CASCADE)
    filetags=models.TextField()

    def __str__(self):
        return f"{self.client.username} - {self.file_id} - {self.file_description}"
    

class CASE(models.Model):
    VICTORY = 'VICTORY'
    DEFEAT = 'DEFEAT'
    STATUS_CHOICES = [  
        (VICTORY, 'Victory'),
        (DEFEAT, 'Defeat'),
    ]
    file=models.ForeignKey(File,on_delete=models.CASCADE)
    case_title=models.CharField(max_length=60,default="New Case")
    lawyer=models.ForeignKey(Lawyer,on_delete=models.CASCADE)
    ratings = models.DecimalField(max_digits=2, decimal_places=1, default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])  # noqa: F821
    case_status=models.CharField(max_length=7, choices=STATUS_CHOICES, default=VICTORY)
    case_approval=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.case_title} - {self.lawyer} - {self.case_approval}"

class Connection(models.Model):
    client=models.ForeignKey(Client,on_delete=models.CASCADE)
    lawyer=models.ForeignKey(Lawyer,on_delete=models.CASCADE)
    case=models.ForeignKey(CASE,on_delete=models.CASCADE)
    connect_status=models.BooleanField(default=False)
    is_removed=models.BooleanField(default=False)
    def save(self, is_removed=False,*args, **kwargs):
        newcase = CASE.objects.get(id=self.case.id)
        if self.connect_status and is_removed is False:
            newcase.case_approval=True
            newcase.save()
        super().save(*args, **kwargs)
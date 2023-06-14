from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

SEX = [
    ("Male",'m'),
    ("Female",'f')
]
class Customer(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    phone_number = PhoneNumberField(unique=True,null=True)
    sex = models.CharField(max_length=10,choices=SEX,default='Male')
    university = models.CharField(max_length=255,null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.phone_number}'
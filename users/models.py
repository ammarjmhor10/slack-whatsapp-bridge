from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

SEX = [
    ("Male",'m'),
    ("Female",'f')
]
class Customer(models.Model):
    phone_number = PhoneNumberField(unique=True,null=True)
    sex = models.CharField(max_length=10,choices=SEX,default='Male')
    university = models.CharField(max_length=255,null=True,blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    nickname = models.CharField(max_length=255,null=True,blank=True)
    def __str__(self):
        if self.phone_number is not None:
            return f'{self.phone_number}'
        else:
            return "Unnamed"
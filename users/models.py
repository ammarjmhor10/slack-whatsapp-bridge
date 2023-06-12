from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

SEX = [
    ("Male",'m'),
    ("Female",'f')
]
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    phone = models.CharField(max_length=15, blank=True)
    sex = models.CharField(max_length=10,choices=SEX,default='Male')
    university = models.CharField(max_length=255,null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    
    @property
    def phone_number(self) -> str:
        if self.phone.startswith('0'):
            return '966'+ self.phone[1:] 
        elif self.phone.startswith('5'):
            return '966' + self.phone 
        elif self.phone.startswith('+'):
            return self.phone.replace('+','')
        else :
            return self.phone
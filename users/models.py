from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# from slack_bridge.models import MessageSlackBridge

# Create your models here.

SEX = [
    ("Male",'m'),
    ("Female",'f')
]
class Customer(models.Model):
    # from slack_bridge.models import MessageSlackBridge
    # user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    phone_number = PhoneNumberField(unique=True,null=True)
    sex = models.CharField(max_length=10,choices=SEX,default='Male')
    university = models.CharField(max_length=255,null=True,blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    message_info = models.OneToOneField(MessageSlackBridge,null=True,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f'{self.phone_number}'
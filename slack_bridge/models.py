from django.db import models
from users.models import Customer
# Create your models here.
class ChatSlack(models.Model):
    channel_id = models.CharField(max_length=255,primary_key=True)
    customer  = models.ForeignKey(Customer,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    
class MessageSlack(models.Model):
    ts = models.CharField(("message_id"), max_length=255,primary_key=True)
    channel = models.ForeignKey(ChatSlack,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
from django.db import models
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from users.models import Customer

# Create your models here.
class ChatSlack(models.Model):
    channel_id = models.CharField(max_length=255,primary_key=True)
    customer  = models.ForeignKey(Customer,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    message_info = models.TextField(verbose_name='message_info',null=True)
    message_id_info = models.CharField(("message_id"), max_length=255,unique=True,null=True)
    
    def __str__(self) -> str:
        return f'{self.customer.phone_number}'
class MessageSlackBridge(models.Model):
    UNCOMPLETED = 'U'
    PENDING = 'P'
    COMPLETED = 'C'
    SENT = 'S'
    DELIVERED = 'D'
    READ = 'R'
    FAILED = 'F'
    MARKETING = 'M'
    SERVICE = 'H'
    STATUS_CHOICES = ((COMPLETED, _('completed')),
                       (SENT, _('sent')),
                       (DELIVERED,_('delivered')),
                        (READ, _('read')),
                        (UNCOMPLETED, _('uncompleted')),
                        (FAILED, _('failed')))
    MESSAGE_CHOICES = ((MARKETING, _('marketing')),
                       (SERVICE, _('service')))
    ts = models.CharField(("message_id"), max_length=255,unique=True)
    channel = models.ForeignKey(ChatSlack,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now())
    message_status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=COMPLETED)
    wamid = models.TextField(verbose_name='whatsapp_message_id',null=True)
    message_type = models.CharField(max_length=1,choices=MESSAGE_CHOICES,default=SERVICE)
    message_content = models.TextField(verbose_name='message_content',null=True)
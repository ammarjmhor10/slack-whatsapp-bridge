from django.contrib import admin
from .models import ChatSlack,MessageSlackBridge
import os 
# Register your models here.
admin.site.site_header = os.environ.get('SITE_HEADERS',default=admin.site.site_header)
admin.site.register(ChatSlack)
admin.site.register(MessageSlackBridge)
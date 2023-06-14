from django.contrib import admin
from .models import ChatSlack,MessageSlackBridge
# Register your models here.
admin.site.register(ChatSlack)
admin.site.register(MessageSlackBridge)
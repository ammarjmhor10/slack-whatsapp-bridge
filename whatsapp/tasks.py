from celery import shared_task
import slack 
from slack_bridge.models import ChatSlack,MessageSlackBridge
from users.models import Customer
import os 
from phonenumber_field.phonenumber import phonenumbers
from whatsapp.whatsapp_handler import WhatAppMediaExtracter
from . import utils

@shared_task
def send_slack_message(number,name,data=None):
    number = str('+')+number
    pn = phonenumbers.parse(number)
    s =slack.WebClient(token=os.environ.get('SLACK_TOKEN'))
    notavailble = Customer.objects.get_or_create(phone_number=pn)
    c = notavailble[0]
        
    t = utils.check_chat_slack(customer=c
                                ,s=s
                                ,pn=pn
                                ,name=name
                                ,data_message=data)
    return t    
                
   
@shared_task
def status_message(ts,status,number,error=None):
    number = str('+')+number
    pn = phonenumbers.parse(number)
    s =slack.WebClient(token=os.environ.get('SLACK_TOKEN'))
    notavailble = Customer.objects.get_or_create(phone_number=pn)
    m = MessageSlackBridge.objects.filter(wamid=ts).first()

    ch = ChatSlack.objects.filter(customer=notavailble[0]).first()
    c = notavailble[0]
    if not notavailble[1] and ch and m : 
        ch = ChatSlack.objects.get_or_create(customer=notavailble[0])[0]
        m = MessageSlackBridge.objects.get_or_create(channel=ch,ts=m.ts,wamid=ts)[0]
        re = utils.update_message_status(m=m,ch=ch,status=status,s=s,error=error)
        return re 
    else:
        if status != 'sent' and not m :
            chat = utils.check_chat_slack(customer=c
                                            ,s=s
                                            ,pn=pn
                                            ,name=c.nickname
                                            ,data_message=':mega: from US'
                                            ,status=status
                                            ,waimd=ts
                                            ,error=error)
            return chat 
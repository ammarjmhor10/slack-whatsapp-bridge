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
    if notavailble[1]:
        r = s.conversations_create(name='n-'+str(pn.national_number))
        customer_info = 'name On Whatsapp: '+str(name)+'\n'+'number: ' + str(pn.country_code)+str(pn.national_number) + '\n' 
        if r['ok']:
            ch = r['channel']['id']
            customer = Customer.objects 
            pinned_message = s.chat_postMessage(channel=ch,text=customer_info)
            pinned = s.pins_add(channel=ch,timestamp=pinned_message['ts'])
            chat = ChatSlack.objects.create(channel_id=ch,customer=notavailble[0])
            s.conversations_invite(channel=ch,users=['U04692A0Y87','U05CHHUS5CG','U05CE5ZEENR','U05CHUU129Z'])
            if data['type']=='text':
                s.chat_postMessage(channel=ch,text=data['text']['body'])
                return 'done'
            else:
                media_data = data[data['type']]
                mime_type = media_data['mime_type']
                media_id  = media_data['id']
                content = WhatAppMediaExtracter().get_media(media_id=media_id)
                s.files_upload(channel=ch,content=content)
                return 'done uploading'
                
                
    else:
        ch = ChatSlack.objects.filter(customer=notavailble[0]).first()
        if data['type']=='text' and ch:
                s.chat_postMessage(channel=ch.channel_id,text=data['text']['body'])
                return 'done' 
        else:
            media_data = data[data['type']]
            mime_type = media_data['mime_type']
            media_id  = media_data['id']
            extract = WhatAppMediaExtracter()
            content = extract.get_media(media_id=media_id)
            f = s.files_upload(channels=ch.channel_id,content=content)
            return 


@shared_task
def status_message(ts,status,number):
    number = str('+')+number
    pn = phonenumbers.parse(number)
    s =slack.WebClient(token=os.environ.get('SLACK_TOKEN'))
    notavailble = Customer.objects.get_or_create(phone_number=pn)
    # return notavailble
    m = MessageSlackBridge.objects.filter(wamid=ts).first()
    customer_info = 'name On Whatsapp: '+'Unknown'+'\n'+'number: ' + str(pn.country_code)+str(pn.national_number) + '\n' 
    if notavailble[1] and not m:
        r = s.conversations_create(name='n-'+str(pn.national_number))
        ch = r['channel']['id']
        pinned_message = s.chat_postMessage(channel=ch,text=customer_info)
        pinned = s.pins_add(channel=ch,timestamp=pinned_message['ts'])
        chat = ChatSlack.objects.get_or_create(channel_id=ch,customer=notavailble[0],message_id_info=pinned_message['ts'])[0]
        marketing_message = s.chat_postMessage(channel=ch,text='message from out slack to this customer')
        m = MessageSlackBridge.objects.get_or_create(channel=chat,ts=marketing_message['ts'],message_type=MessageSlackBridge.MARKETING)[0]
        s.conversations_invite(channel=ch,users=['U04692A0Y87','U05CHHUS5CG'])
        re = utils.update_message_status(m=m,ch=chat,status=status,s=s)
        return re 
    if not notavailble[1] and not m : 
        ch = ChatSlack.objects.get_or_create(customer=notavailble[0])[0]
        marketing_message = s.chat_postMessage(channel=ch.channel_id,text='message from out slack to this customer')
        m = MessageSlackBridge.objects.get_or_create(channel=ch,ts=marketing_message['ts'],message_type=MessageSlackBridge.MARKETING,wamid=ts)[0]
        re = utils.update_message_status(m=m,ch=ch,status=status,s=s)
        return re 
    if not notavailble[1] and m : 
        ch = ChatSlack.objects.get_or_create(customer=notavailble[0])[0]
        # marketing_message = s.chat_postMessage(channel=ch.channel_id,text='message from out slack to this customer')
        m = MessageSlackBridge.objects.get_or_create(channel=ch,ts=m.ts,message_type=MessageSlackBridge.SERVICE,wamid=ts)[0]
        re = utils.update_message_status(m=m,ch=ch,status=status,s=s)
        return re 
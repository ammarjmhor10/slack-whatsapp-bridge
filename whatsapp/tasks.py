from celery import shared_task
import slack 
from slack_bridge.models import ChatSlack,MessageSlackBridge
from users.models import Customer
import os 
from phonenumber_field.phonenumber import phonenumbers
from whatsapp.whatsapp_handler import WhatAppMediaExtracter

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
    m =  MessageSlackBridge.objects.get(wamid=ts)
    d = 'd'
    r = 'r'
    f = 'f'
    ch = ChatSlack.objects.get_or_create(channel_id=str(m.channel.channel_id),)
    customer_info = 'name On Whatsapp: '+'Unknown'+'\n'+'number: ' + str(pn.country_code)+str(pn.national_number) + '\n' 
    if notavailble[1]:
        r = s.conversations_create(name='n-'+str(pn.national_number))
    if status == 'delivered':
        m.message_status = m.DELIVERED
        m.save()
        s.reactions_add(name='white_check_mark',channel=ch.channel_id,timestamp=m.ts)
        return d
    if status == 'read':
        m.message_status = m.READ
        m.save()
        s.reactions_add(name='eyes',channel=ch.channel_id,timestamp=m.ts)
        return r 
    if status == 'failed':
        m.message_status = m.FAILED
        m.save()
        s.reactions_add(name='x',channel=ch.channel_id,timestamp=m.ts)
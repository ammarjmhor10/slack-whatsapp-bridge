# from django.utils.translation import gettext_lazy as _
from slack_bridge.models import MessageSlackBridge,ChatSlack
from users.models import Customer
import slack 
from phonenumber_field.phonenumber import PhoneNumber
from whatsapp.whatsapp_handler import WhatAppMediaExtracter


def update_message_status(m:MessageSlackBridge,ch:ChatSlack,status,s:slack.WebClient):
    # from slack_bridge.models import MessageSlackBridge
    if status == 'delivered':
        m.message_status = "D"
        m.save()
        s.reactions_add(name='white_check_mark',channel=ch.channel_id,timestamp=m.ts)
        return 'd'
    if status == 'read':
        m.message_status = "R"
        m.save()
        s.reactions_add(name='eyes',channel=ch.channel_id,timestamp=m.ts)
        return 'r'
    if status == 'failed':
        m.message_status = "F"
        m.save()
        s.reactions_add(name='x',channel=ch.channel_id,timestamp=m.ts)
        return 'f'


def send_message_slack(data,s:slack.WebClient,ch:ChatSlack,waimd:str,status=None):
    if status:
        m = MessageSlackBridge.objects.filter(channel=ch,wamid=waimd).first()
        if not m: 
            ts = s.chat_postMessage(channel=ch.channel_id,text=data)
            m = MessageSlackBridge.objects.get_or_create(channel=ch,ts=ts['ts'],message_type=MessageSlackBridge.MARKETING,wamid=waimd)
        r = update_message_status(m=m[0],ch=ch,s=s,status=status)
        return 'done'
    if data['type']=='text':
        s.chat_postMessage(channel=ch.channel_id,text=data['text']['body'])
        return 'done'
    else:
        media_data = data[data['type']]
        mime_type = media_data['mime_type']
        media_id  = media_data['id']
        media = WhatAppMediaExtracter()
        media.get_media(media_id=media_id)
        rew = s.files_upload(channels=ch.channel_id,content=media.content)
        return 'done uploading'

def check_chat_slack(customer:Customer,s:slack.WebClient,pn:PhoneNumber,name:str,data_message,status=None,waimd=None):
    ch = ChatSlack.objects.filter(customer=customer).first()
    if not ch:
        r = s.conversations_create(name='n-'+str(pn.national_number))
        name = customer.nickname
        customer_info = 'name On Whatsapp: '+str(name)+'\n'+'number: ' + str(pn.country_code)+str(pn.national_number) + '\n' 
        ch = ChatSlack.objects.create(channel_id=r['channel']['id'],customer=customer)
        pinned_message = s.chat_postMessage(channel=ch.channel_id,text=customer_info)
        pinned = s.pins_add(channel=ch.channel_id,timestamp=pinned_message['ts'])
        s.conversations_invite(channel=ch.channel_id,users=['U04692A0Y87','U05CHHUS5CG','U05CE5ZEENR','U05CHUU129Z'])
        # s.conversations_invite(channel=ch.channel_id,users=['U04692A0Y87','U05CHHUS5CG'])
        ch.message_id_info = pinned_message['ts']
        ch.save()
    send_message = send_message_slack(data=data_message,s=s,ch=ch,waimd=waimd,status=status)
    if customer.nickname != name:
        customer.nickname = name 
        customer.save()
        customer_info = 'name On Whatsapp: '+str(name)+'\n'+'number: ' + str(pn.country_code)+str(pn.national_number) + '\n' 
        ts = ch.message_id_info
        s.chat_update(channel=ch.channel_id,ts=ts,text=customer_info)
    return ch 

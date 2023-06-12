import logging
import os
import requests 
from rest_framework.response import Response
from datetime import datetime
from PIL import Image
import io 
from . import tasks 



class Message:
    message_type:str = None  
    body:str = None 
    meme_type : str = None 
    def __init__(self,message_type,body,meme_type=None) -> None:
        self.message_type = message_type
        self.body = body 
        self.meme_type = meme_type
            

class Transporter:
    def __init__(self,data) -> None:
        self.data = data

    @property
    def valid_slack(self) -> str:
        from .models import ChatSlack,MessageSlack
        if 'token' in self.data and self.data['token'] == os.environ.get('SLACK_VALIDATION_TOKEN','B7MGJbEdFHBOjnT9dz4ySGVV'):
            logging.info('request from slack')
            if 'challenge' in self.data:
                logging.info('verify url')
                return Response({'challenge':self.data['challenge']})
            if 'event' in self.data:
                event = self.data['event'] 
                logging.info('receive event from slack ')
                #check the user only 
                if 'bot_id' not in event and event['type']== 'message':
                    ts = event['ts']
                    channel = event['channel']
                    print(channel)
                    c = ChatSlack.objects.filter(channel_id=channel).exists()
                    print(c)
                    if not c :
                        logging.warning('channel not found in db !!')
                    chat = ChatSlack.objects.filter(channel_id=channel).first()
                    #check files
                    #Documentation https://api.slack.com/events/message/file_share
                    if 'files' in event and c and 'text' in event :
                        file = event['files'][0] 
                        mimetype = file['mimetype']
                        file_url = file['url_private_download']
                        file_id = file['id']
                        # tasks.event.delay(p='966562601855',m=Message(message_type='media',body=file_url,meme_type=mimetype))
                        tasks.event.delay(phone_number=chat.customer.phone_number
                                          ,message_type ='media',body=file_url
                                          ,mime_type=mimetype)
                        # e = slack.WebClient(token='xoxp-4224677615669-4213078032279-5410971369809-9eab07466845e204504b96bc95b981f0')
                        return Response('event received')
                    #check messages 
                    #Documentation https://api.slack.com/events/message
                    if not 'files' in event and 'text' in event and c:
                        ts = event['ts']
                        text= event['text']
                        p =chat.customer.phone_number
                        print(p)
                        tasks.event.delay(phone_number=p
                                          ,message_type ='messages',body=text
                                          ,mime_type=None)
                        logging.info('receive event from a user not the bot')
                        return Response('event received')
            return Response('done')
        else:
            logging.warning('request from not slack be carful')
            return Response('error',status=404)
        
        
class WhatsappSenderMessage:
     def __init__(self,phone_number,message:Message) -> None:
        self.phone_number = phone_number
        self.message      = message
     whatsapp_token = os.environ.get('WHATSAPP_TOKEN','EAAiUrI4L3UkBACyarG4zwqJJYySMwqRZAiFk16PJsqnbthsgQDAtgmS7VZAUvlsAuiVjaOveb02eb685BL97eYNZBFT0AHbDSLf67sZAUQeK0I1MEv05dNJRyWvS3OjCp6q0lNCIee8xvSuBPhNb6YZCElp8sPbp7atLWcH5oxIamMYzHtAqP')
     headers = {
            'Authorization': 'Bearer '+ whatsapp_token,
            }
     message_type = 'messages'
     
     @property
     def url(self):
        return 'https://graph.facebook.com/v13.0/108022628653202/messages'
     
     
     @property
     def body_message(self):
         if self.message.message_type == WhatsappSenderMessage.message_type:
                m = {
                "messaging_product": "whatsapp",
                "to": self.phone_number,
                "type": "text",
                "text": {
                    "body": self.message.body
                }
            }
                return m
         else:
                return WhatsappConverterMedia(self.phone_number,self.message).body_message
    
     def send_message(self):
        r = requests.post(self.url, headers=self.headers, json=self.body_message)
        return r.status_code
    
class WhatsappConverterMedia(WhatsappSenderMessage):
    payload={'messaging_product': 'whatsapp'}
    
     
    def get_media_content(self):
        r = requests.get(url=self.message.body,headers={
            'Authorization': 'Bearer xoxb-4224677615669-5395305320821-mXpJIJh2MvtxtqNtpjcXhxPR',
            }).content
        mime_type = self.message.meme_type.split('/')[0]
        if mime_type == 'image':
            im = Image.open(io.BytesIO(r))
            output_bytes_io = io.BytesIO()
            rgb_im = im.convert('RGB').save(output_bytes_io, format='JPEG')
            return output_bytes_io.getvalue()
        else:
            return r
            
    def media_id(self):
        d = str(datetime.now().timestamp())
        extension = str(self.message.meme_type.split('/')[1])
        files=[
        ('file',(d+extension,self.get_media_content(),self.message.meme_type))
        ]
        payload={'messaging_product': 'whatsapp'}
        r = requests.post(url='https://graph.facebook.com/v13.0/108022628653202/media',headers=self.headers,data=payload,files=files)
        return r.json()['id']
    @property
    def body_message(self):
        t = self.message.meme_type.split("/")[0]
        if t == 'text' or t =='application':
            t = 'document'
            m = {
                    "messaging_product": "whatsapp",
                    "to": self.phone_number,
                    "type": t,
                    t: {
                        'id': self.media_id()
                    }}
            return m 
        else:
             m = {
                    "messaging_product": "whatsapp",
                    "to": self.phone_number,
                    "type": t,
                    t: {
                        'id': self.media_id()
                    }}
             return m 


        
        
if __name__ == '__main__' :
    m = Message('media','https://files.slack.com/files-pri/T046LKXJ3KP-F05CK8KFFQQ/screenshot_1444-10-16_at_10.06.10_pm.png','image/jpeg')
    w = WhatsappSenderMessage('966562601855',m)
    print(w.send_message())
    # pass 
import os 
from slack_bridge.events import Message
import requests
from PIL import Image
import io 
from datetime import datetime



class WhatsappSenderMessage:
     def __init__(self,phone_number=None,message:Message=None) -> None:
        self.phone_number = phone_number
        self.message      = message
     whatsapp_token = os.environ.get('WHATSAPP_TOKEN')
     whatsapp_phone_id = os.environ.get('WHATSAPP_PHONE_NUMBER_ID')
     whatsapp_version_api = os.environ.get('WHATSAPP_VERSION_API')
     whatsapp_url = 'https://graph.facebook.com'
     waid = None 
     headers = {
            'Authorization': 'Bearer '+ whatsapp_token,
            }
     message_type = 'messages'
     
     @property
     def url(self):
        return f'{self.whatsapp_url}/{self.whatsapp_version_api}/{self.whatsapp_phone_id}/messages'
     
     
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
     @property
     def send_message(self)->str:
        r = requests.post(self.url, headers=self.headers, json=self.body_message)
        if r.status_code == 200:
            self.waid = r.json()['messages'][0]['id']
            return 'ok'
        else:
            return None 
        
        
     

class WhatsappConverterMedia(WhatsappSenderMessage):
    payload={'messaging_product': 'whatsapp'}
    
    @property
    def url(self):
        return f'{self.whatsapp_url}/{self.whatsapp_version_api}/{self.whatsapp_phone_id}/media'
     
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
        r = requests.post(url=self.url,headers=self.headers,data=payload,files=files)
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


        

class WhatAppMediaExtracter(WhatsappSenderMessage):
    content = None 
    def get_media(self,media_id):
          url = f'{self.whatsapp_url}/{self.whatsapp_version_api}/{media_id}'
          r = requests.get(url=url,headers=self.headers)
          content = requests.get(r.json()['url'],headers=self.headers)
          if content.status_code == 200:
              self.content = content.content
              return content.content
          return None 

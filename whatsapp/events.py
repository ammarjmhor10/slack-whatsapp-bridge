import logging
from rest_framework.response import Response
import os 
from phonenumber_field.phonenumber import phonenumbers
# from slack_bridge.models import ChatSlack
# from users.models import Customer
import slack 
from . import tasks 
class WhatsAppReceiver:
    def __init__(self,data) -> None:
        self.data = data 
        
        
    @property    
    def valid_whatsapp(self):
        if 'object' in self.data and self.data['entry'][0]['id'] == os.environ.get('WHATSAPP_WA_ID'):
                wah_data = self.data['entry'][0]['changes'][0]['value']
                # number = wah_data['metadata']['display_phone_number']
                if 'messages' in wah_data:
                    msg = wah_data['messages'][0]
                    name = wah_data['contacts'][0]['profile']['name']
                    number = msg['from']
                    content_type = msg['type']
                    tasks.send_slack_message.delay(number,name,msg)
                    return Response('done')
                if 'statuses' in wah_data:
                    status_data = dict(wah_data['statuses'][0])
                    status = status_data['status']
                    waid = status_data['id']
                    number = status_data['recipient_id']
                    errors = status_data.get('errors')
                    print(errors)
                    tasks.status_message.delay(waid,status,number,errors)
                    # print(waid,status)
                    return Response('done')
                    
        else:
            logging.warning('not from whatsapp')
            return Response('not allowed',status=403)
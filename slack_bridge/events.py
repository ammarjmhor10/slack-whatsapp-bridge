import logging
import os
from rest_framework.response import Response
from . import tasks 
import emoji_data_python


class Message:
    message_type:str = None  
    body:str = None 
    meme_type : str = None 
    ts : str = None 
    def __init__(self,message_type,body,ts,meme_type=None) -> None:
        self.message_type = message_type
        self.body = body 
        self.meme_type = meme_type
        self.ts = ts     

class Transporter:
    def __init__(self,data:dict) -> None:
        self.data = data
    
    
    def extract_text(self,text:dict):
        message = ''
        text_type = dict(text).get('text')
        emoji_type = text.get('unicode')
        if emoji_type != None:
            return message +  ':'+str(text['name'])+":"
        if text_type != None:
            return message + str(text_type)
        else:
            return message 
    @property
    def valid_slack(self) -> str:
        from .models import ChatSlack,MessageSlackBridge
        if 'token' in self.data and self.data['token'] == os.environ.get('SLACK_VALIDATION_TOKEN'):
            logging.info('request from slack')
            if 'challenge' in self.data:
                logging.info('verify url')
                return Response({'challenge':self.data['challenge']})
            if 'event' in self.data:
                #Documentation https://api.slack.com/events
                event = dict(self.data['event'])
                logging.info('receive event from slack ')
                #check the user only 
                if  'bot_id' not in event and event['type'] == 'message' and event.get('subtype') != 'channel_join' and event.get('user') != 'U05BM8Z9EQ5':
                    ts = event['ts']
                    channel = event['channel']
                    slack_channel_id  = ChatSlack.objects.filter(channel_id=channel).exists()
                    if not slack_channel_id :
                        logging.warning('channel not found in db !!')
                        return Response('ok')
                    chat = ChatSlack.objects.get(channel_id=channel)
                    p = chat.customer.phone_number
                    slack_message_ts  = MessageSlackBridge.objects.get_or_create(ts=ts,channel=chat)
                    #check files
                    #Documentation https://api.slack.com/events/message/file_share
                    if 'files' in event and slack_channel_id and event.get('subtype') == 'file_share' :
                        file = event['files'][0] 
                        mimetype = file['mimetype']
                        file_url = file['url_private_download']
                        tasks.event.delay(phone_number=str(p)
                                          ,message_type ='media',body=file_url
                                          ,mime_type=mimetype,ts=str(ts))
                        return Response('event file received')
                    #check messages 
                    #Documentation https://api.slack.com/events/message
                    if not 'files' in event and 'text' in event and slack_channel_id:
                        ts = event['ts']
                        blocks = event['blocks'][0]
                        elements = blocks['elements'][0]
                        text = ''.join([self.extract_text(text) for text in elements['elements'] ])
                        p = chat.customer.phone_number
                        tasks.event.delay(phone_number=str(p)
                                          ,message_type ='messages',body=emoji_data_python.replace_colons(text)
                                          ,mime_type=None,ts=str(ts))
                        logging.info('receive event from a user not the bot')
                        return Response('event text received')
                if event['type'] =='channel_deleted':
                    channel = event['channel']
                    slack_channel_id  = ChatSlack.objects.filter(channel_id=channel).exists()
                    if not slack_channel_id :
                        logging.warning('channel not found in db !!')
                        return Response('ok')
                    chat = ChatSlack.objects.get(channel_id=channel)
                    chat.delete()
                    return Response('deleted')
            return Response('done')
        else:
            logging.warning('request from not slack be carful!')
            return Response('error',status=403)
        
    
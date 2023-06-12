from celery import shared_task
from .events import Message,WhatsappSenderMessage

@shared_task
def event(phone_number,message_type,body,mime_type):
    mm = None if not mime_type else mime_type
    m = Message(message_type=message_type,body=body,meme_type=mm)
    w = WhatsappSenderMessage(phone_number=phone_number,message=m)
    w.send_message()
    return w



from celery import shared_task
from . import events


@shared_task
def event(phone_number,message_type,body,mime_type,ts):
    from whatsapp.whatsapp_handler import WhatsappSenderMessage
    from slack_bridge.models import MessageSlackBridge
    mm = None if not mime_type else mime_type
    m = events.Message(message_type=message_type,body=body,meme_type=mm,ts=ts)
    w = WhatsappSenderMessage(phone_number=phone_number,message=m)
    waid = str(w.send_message)
    if not waid:
        message = MessageSlackBridge.objects.get(ts=ts)
        message.message_status = message.UNCOMPLETED
        message.save()
        return 'task error'
    else:
        message = MessageSlackBridge.objects.get(ts=ts)
        message.wamid = w.waid
        message.save()
        return 'task done'

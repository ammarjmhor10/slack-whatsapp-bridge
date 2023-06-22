# from django.utils.translation import gettext_lazy as _
from slack_bridge.models import MessageSlackBridge,ChatSlack
import slack 




def update_message_status(m:MessageSlackBridge,ch:ChatSlack,status,s:slack.WebClient):
    # from slack_bridge.models import MessageSlackBridge
    if status == 'delivered':
        m.message_status = "R"
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

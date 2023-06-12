from django.shortcuts import render
# from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import slack 
import requests 
from .events  import Transporter
# Create your views here.


# class Challenge(APIView):
#     data1 = 
@api_view(["GET","POST"])
def challnge(request,*args, **kwargs):
    if request.method == 'GET':
        return Response('test')
    elif request.method == 'POST':
        data = request.data 
        # print(data)
        r = Transporter(data)
        
        # if data['event'] == 'send_message':
        #     e = slack.WebClient(token='xoxb-4224677615669-5395305320821-mXpJIJh2MvtxtqNtpjcXhxPR')
        # #     # e.conversations_invite(channel='C05B9UVJ9V5',users="U05BM8Z9EQ5")
        #     e.chat_postMessage(channel='C04727SKUNM',text='hi from bot')
        #     r = requests.get(url='https://storage.googleapis.com/rocket-chat-bridge/1009716280418913.jpeg').content
        #     # e.files_upload(content=r)
            
        #     # print(e.files_upload(channels='C04727SKUNM',content=r))
        #     e.reactions_add(name='eyes',channel='C04727SKUNM',timestamp='1686326584.095539')
        return r.valid_slack
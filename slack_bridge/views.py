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
        
        if 'event' in data and data['event'] == 'send_message':
            return ResourceWarning('ok')
        r = Transporter(data)
        return r.valid_slack
        return Response('done')
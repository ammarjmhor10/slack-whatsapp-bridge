from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.http import HttpRequest,HttpResponse
import os 
from whatsapp.events import WhatsAppReceiver
# Create your views here.

class WhatsAppTest(APIView):
       """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
       
       def verify_token(self,par:dict):
           """Verify Token Whatsapp
           Documentation https://developers.facebook.com/docs/graph-api/webhooks/getting-started#verification-requests

           Args:
               par (dict): _description_

           Returns:
               _type_: _description_
               
           """
           secret = os.environ.get('SECRET_WHATSAPP')
           if 'hub.challenge' in par :
                # return HttpResponse(self.verify_token(r))
                if secret == par['hub.verify_token']:
                    return par['hub.challenge']
           else:
               return None 
       def get(self,request:Request):
            par = request.query_params.dict()
            v = self.verify_token(par)
            if v :
                return HttpResponse(v)    
            return Response('not allwoed !',status=403)
       def post(self, request:Request, format=None):
            """
            receive whatsapp messages.
            """
            data = request.data
            print(data)
            r = WhatsAppReceiver(data)
            return r.valid_whatsapp 


# @api_view(['POST'])
# def whatsapp_api(request:Request,*args, **kwargs):
#     d = request.data
#     return Response('data')
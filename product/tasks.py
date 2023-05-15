# Create your tasks here
from __future__ import absolute_import,unicode_literals
from celery import shared_task
import requests 
from time import sleep
@shared_task
def add():
    r = requests.get('https://webhook.site/21b3223f-49c9-44ba-a03b-ca62e50f3774')
    return 'l'

@shared_task
def multi(x, y):
    print(x,y)
    sleep(5)
    return x * y + 2 


@shared_task
def minus(x, y):
    print(x,y)
    return x - y+ 2 

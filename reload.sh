#!/bin/bash

sudo systemctl restart django.service && sudo systemctl restart django.socket && sudo systemctl restart celery.service && sudo systemctl restart celerybeat.service && echo "done"
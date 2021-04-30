from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from rest_framework.decorators import api_view

from .models import InstagramUser
from .serializers import InstagramUserSerializer

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time
from selenium.webdriver.common.keys import Keys
import requests, re
import json


from celery import shared_task
from celery.decorators import task
from .celery import insta_scrapper

@api_view(['POST'])
def user_scrapper_post(request):
    tag = JSONParser().parse(request)
    hashTag = '#'+tag['hashtag']
    if request.method == 'POST':
        task = insta_scrapper.delay('YOUR USERNAME',"YOUR PASSWORD",hashTag)
        return JsonResponse({"task_id":task.task_id},safe=False)

@api_view(['GET'])
def user_scrapper_get(request,tag):
    if request.method == 'GET':
        hashTag = '#'+tag
        users = InstagramUser.objects.all().filter(hash_tag=hashTag)
        user_serializer = InstagramUserSerializer(users,many=True)
        print(user_serializer.data)
        return JsonResponse(user_serializer.data,safe=False)




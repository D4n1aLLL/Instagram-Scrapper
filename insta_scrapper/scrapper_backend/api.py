from rest_framework import viewsets
from Scrapper import insta_scrapper
from .serializers import InstagramUserSerializer
from .models import InstagramUser

class InstagramUserViewSet(viewsets.ModelViewSet):
    serializer_class = InstagramUserSerializer
    queryset = InstagramUser.objects.all()

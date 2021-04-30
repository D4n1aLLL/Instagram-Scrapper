from django.conf.urls import url 
from . import views 
 
urlpatterns = [ 
    url(r'^api/hashtag/(?P<tag>\w+)$', views.user_scrapper_get),
    url(r'^api/hashtag/$', views.user_scrapper_post),
]

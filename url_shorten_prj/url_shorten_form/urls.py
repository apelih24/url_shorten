from django.conf.urls import url
from .views import get_url, redirect_user

app_name = 'url_shorten_form'

urlpatterns = [
    url(r'^shorten/', get_url),
    url(r'^(?P<url>[\w\-]+)/$', redirect_user)
]

from django.conf.urls import url
from .views import ShortFormView, redirect_user

app_name = 'url_shorten'

urlpatterns = [
    url(r'^shorten/', ShortFormView.as_view()),
    url(r'^(?P<url>[\w\-]+)/$', redirect_user)
]

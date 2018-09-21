# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from .forms import URLForm
from .models import URLModel
from .utils import to_base62


class ShortFormView(View):
    form_class = URLForm
    index_template = 'url_shorten/index.html'
    response_template = 'url_shorten/response.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'url_shorten/index.html', {'form': form})

    def post(self, request, *args, **kwargs):
        host = request.scheme + '://' + request.META['HTTP_HOST'] + '/'
        encoded_url = host
        msg = None

        form = URLForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            if not data['user_hash']:
                url = data['user_url']

                url_from_model = URLModel.objects.filter(original_url=url)
                if not url_from_model.exists():
                    original_url = URLModel(original_url=url)
                    original_url.save()
                    original_url.hash = to_base62(original_url.pk)
                    original_url.save()

                    encoded_url = host + to_base62(original_url.pk) + '/'
                else:
                    msg = 'This link has already been shorted with another hash'
                    encoded_url = host + url_from_model[0].hash + '/'
            else:
                hash = URLModel.objects.filter(hash=data['user_hash'])
                if hash.exists():
                    return HttpResponse(data['user_hash'] + ' hash has already been taken')

                url = data['user_url']

                url_from_model = URLModel.objects.filter(original_url=url)

                if not url_from_model.exists():
                    original_url = URLModel(original_url=url)
                    original_url.save()
                    original_url.hash = data['user_hash']
                    original_url.save()

                    encoded_url = host + data['user_hash'] + '/'
                else:
                    msg = 'This link has already been shorted with another hash'
                    encoded_url = host + url_from_model[0].hash + '/'

            if msg:
                return render(request, self.response_template, {'msg': msg, 'url': encoded_url})
            return render(request, self.response_template, {'msg': msg, 'url': encoded_url})


def redirect_user(request, url):
    host = request.scheme + '://' + request.META['HTTP_HOST'] + '/'
    original_url = host
    shorten = URLModel.objects.filter(hash=url)
    if shorten:
        return redirect(shorten[0].original_url)
    return redirect(original_url)

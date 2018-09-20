# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from math import floor
from string import ascii_lowercase, ascii_uppercase
import string

from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import URLForm
from .models import OriginalURL, ShortenedURL

host = 'http://127.0.0.1:8000/'


def to_base62(num, b=62):
    if b <= 0 or b > 62:
        return 0
    base = string.digits + ascii_lowercase + ascii_uppercase
    r = num % b
    res = base[r]
    q = floor(num / b)
    while q:
        r = q % b
        q = floor(q / b)
        res = base[int(r)] + res
    return res


def get_url(request):
    if request.method == 'POST':
        encoded_url = host
        msg = None

        form = URLForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            if not data['user_hash']:
                url = data['user_url']

                url_from_model = OriginalURL.objects.filter(url=url)
                if not url_from_model.exists():
                    original_url = OriginalURL(url=url)
                    original_url.save()

                    encoded_url = host + to_base62(original_url.pk) + '/'

                    shortened_url = ShortenedURL(original=original_url, hash=to_base62(original_url.pk))
                    shortened_url.save()
                else:
                    msg = 'This link has already been shorted with another hash'
                    encoded_url = host + url_from_model[0].shortenedurl.hash + '/'
            else:
                hash = ShortenedURL.objects.filter(hash=data['user_hash'])
                if hash.exists():
                    return HttpResponse(data['user_hash'] + ' has already been taken')

                url = data['user_url']

                url_from_model = OriginalURL.objects.filter(url=url)

                if not url_from_model.exists():
                    original_url = OriginalURL(url=url)
                    original_url.save()

                    encoded_url = host + data['user_hash'] + '/'

                    shortened_url = ShortenedURL(original=original_url, hash=data['user_hash'])
                    shortened_url.save()
                else:
                    msg = 'This link has already been shorted with another hash'
                    encoded_url = host + url_from_model[0].shortenedurl.hash + '/'

            if msg:
                return HttpResponse("{}: <a href='{}'>{}</a>".format(msg, encoded_url, encoded_url))

            return HttpResponse("<a href='{}'>{}</a>".format(encoded_url, encoded_url))

    else:
        form = URLForm()

    return render(request, 'url_shorten_form/index.html', {'form': form})


def redirect_user(request, url):
    original_url = host
    shorten = ShortenedURL.objects.filter(hash=url)
    if shorten:
        original_url = OriginalURL.objects.get(shortenedurl=shorten[0])
    return redirect(original_url.url)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class OriginalURL(models.Model):
    url = models.URLField(
        max_length=100,
        blank=False,
        null=False
    )


class ShortenedURL(models.Model):
    original = models.OneToOneField(
        OriginalURL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    hash = models.CharField(max_length=15, blank=False, null=False)


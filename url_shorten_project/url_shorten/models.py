# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class URLModel(models.Model):
    original_url = models.URLField(
        max_length=100,
        blank=False,
        null=False
    )
    hash = models.CharField(max_length=15, blank=False, null=False)

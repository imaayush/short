# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.core.validators import URLValidator
from .utils import generate_random_id


class ShortenerManager(BaseUserManager):

    def expand(self, short_url):
        """
        Expands a provided short URL, i.e., returns the original URL
        """
        try:
            return self.get(short_url=short_url).url
        except Shortener.DoesNotExist:
            pass

    def shorten(self, url=None, **kwargs):
        """
        Shortens a provided URL
        """
        val = URLValidator()
        val(url)

        # Make a new one
        short_url = generate_random_id()

        url_list = self.filter(url=url)

        if url_list:
            return url_list[0]
        else:
            return self.create(url=url, short_url=short_url)


class Shortener(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    url = models.URLField(('Original URL'))
    short_url = models.URLField(('Shortened URL'), unique=True,)
    objects = ShortenerManager()

    class Meta:
        ordering = ('created',)


from __future__ import absolute_import, print_function, unicode_literals

import logging
import re
import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from shortener.models import Shortener
from .serializers import ShortenerUrlSerializer


class ExpandUrlView(APIView):

    def get(self, request, *args, **kwargs):
        url = self.kwargs['uuid']
        url = Shortener.objects.expand(url)
        if url is None:
            raise exceptions.NotFound(['url not found'])

        return redirect(url)


class ShortenerUrlView(APIView):
    serializers_class = ShortenerUrlSerializer

    def post(self, request, *args, **kwargs):
        url = request.data.get('url')
        try:
            shorten_url = Shortener.objects.shorten(url)
        except ValidationError, e:
            raise exceptions.ValidationError(detail = e.message)

        serializer = ShortenerUrlSerializer(shorten_url)

        return Response(serializer.data)

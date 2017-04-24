from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import url
from django.http import Http404

from . import views

urlpatterns = [
    url(r'^short/$',
        views.ShortenerUrlView.as_view(), name='short-url'),

    url(r'^(?P<uuid>[a-zA-Z0-9-]+)/$',
        views.ExpandUrlView.as_view(), name='expand-url'),
]


def unknown_api_endpoint(request):
    raise Http404("Unknown API endpoint")

urlpatterns += [
    url(r'', unknown_api_endpoint, name='unknown-api-endpoint')
]

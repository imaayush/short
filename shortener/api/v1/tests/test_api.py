from rest_framework import status

from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from shortener.models import Shortener
from shortener.utils import generate_random_id, DEFAULT_SHORT_LEN

SHORT_URL = 'short-url'
EXPAND_URL = 'expand-url'


class UrlShortenerTestCase(APITestCase):
    def test_url_shortener_for_vaild_url(self):
        url = "https://google.com"
        shortener = Shortener.objects.shorten(url)
        request_url = reverse(SHORT_URL)
        data = {'url': url}
        response = self.client.post(request_url, data=data, format='json')
        self.assertEqual(response.data['url'], shortener.url)
        self.assertEqual(response.data['short_url'], shortener.short_url)
        self.assertEqual(len(response.data['short_url']), DEFAULT_SHORT_LEN)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_shortener_for_invaild_url(self):
        url = "https//google.com"
        request_url = reverse(SHORT_URL)
        data = {'url': url}
        response = self.client.post(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], 'Enter a valid URL.')

    def test_url_shoretener_unique(self):
        request_url = reverse(SHORT_URL)
        urls = ["https://google{}.com".format(i) for i in range(0, 100)]
        short_urls = []

        for url in urls:
            data = {'url': url}
            response = self.client.post(request_url, data=data, format='json')
            short_urls.append(response.data['short_url'])

        unique_urls = set(short_urls)

        self.assertEqual(len(unique_urls), len(short_urls))


class UrlExpandTestCase(APITestCase):
    def test_url_expand_for_exist_short_url(self):
        url = "https://google.com"
        shortener = Shortener.objects.shorten(url)
        request_url = reverse(EXPAND_URL, kwargs={'uuid': shortener.short_url})
        response = self.client.get(request_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, url)

    def test_url_expand_for_no_exist_short_url(self):
        rnd_id = generate_random_id()
        request_url = reverse(EXPAND_URL, kwargs={'uuid': rnd_id})
        response = self.client.get(request_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data[0], 'url not found')


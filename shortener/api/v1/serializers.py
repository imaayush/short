
from rest_framework import serializers
from shortener.models import Shortener


class ShortenerUrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shortener
        fields = ('url', 'short_url')

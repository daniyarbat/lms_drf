import re
from rest_framework.serializers import ValidationError


class UrlValidator:

    def __init__(self, url):
        self.url = url

    def __call__(self, value):
        temp_val = dict(value).get(self.url)
        if temp_val:
            if "youtube.com" not in temp_val:
                raise ValidationError('URL is forbidden')

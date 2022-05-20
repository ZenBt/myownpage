from datetime import datetime
from hashlib import md5
from ..models import ShortUrl
from typing import Union

BASE_SHORTER_URL = '127.0.0.1:8000/l/'

def already_exists(func):
    def wrapper(*args, **kwargs):
        temp_url: ShortUrl = ShortUrl.objects.filter(initial_url=kwargs['url']).first()
        if temp_url:
            return temp_url.short_url
        return func(kwargs['url'])
    return wrapper
            

@already_exists
def shortify(url: str) -> str:
    while True:
        temp_url = url + str(datetime.now)
        short_url = md5(temp_url.encode()).hexdigest()[:6]
        if ShortUrl.objects.filter(short_url=short_url).first() is None:
            add_to_db(short_url=short_url, url=url)
            return short_url

def get_full_link(short_url: str) -> Union[str, None]:
    return ShortUrl.objects.filter(short_url=short_url).first()


def add_to_db(short_url: str, url: str) -> None:
    new_link = ShortUrl(short_url=short_url, initial_url=url)
    new_link.save()

def get_redirect_url(url):
    url = get_full_link(url)
    if url:
        return url.initial_url
    return f'http://{BASE_SHORTER_URL}'

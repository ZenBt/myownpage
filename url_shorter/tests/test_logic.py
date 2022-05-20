from django.test import TestCase

from ..models import ShortUrl
from ..services.api_urlshorter import *

class UrlShorterApiTestCase(TestCase):
    
    def setUp(self):
        self.test_initial_url = 'https://example.com/example'
        self.test_short_url = '34cda2'
        self.test_initial_url2 = 'https://example.com/example2'
        self.test_short_url2 = 'qqc7a2'
        self.test_short_wrong_url = '123456'
        self.short_url_obj = ShortUrl.objects.create(short_url=self.test_short_url,
                                                     initial_url=self.test_initial_url)
    
    def test_one_url_exists(self):
        self.assertEqual(len(ShortUrl.objects.all()), 1)
    
    def test_get_full_link(self):
        response = get_full_link(self.test_short_url).initial_url
        self.assertEqual(response, self.test_initial_url)
    
    def test_get_full_link_with_wrong_url(self):
        response = get_full_link(self.test_short_wrong_url)
        self.assertEqual(response, None)
    
    def test_add_to_db(self):
        self.assertEqual(len(ShortUrl.objects.all()), 1)
        add_to_db(short_url=self.test_short_url2, url=self.test_initial_url2)
        self.assertEqual(len(ShortUrl.objects.all()), 2)
    
    def test_get_redirect_url(self):
        redirect_url = get_redirect_url(self.test_short_url)
        self.assertEqual(redirect_url, self.test_initial_url)
    
    def test_get_redirect_url_with_wrong_url(self):
        redirect_url = get_redirect_url(self.test_short_wrong_url)
        self.assertEqual(redirect_url, f'http://{BASE_SHORTER_URL}')
    
    def test_shortify_already_exists(self):
        self.assertEqual(len(ShortUrl.objects.all()), 1)
        short_url = shortify(url=self.test_initial_url)
        self.assertEqual(len(ShortUrl.objects.all()), 1)
        self.assertEqual(short_url, self.test_short_url)
    
    def test_shortify_doesnt_exists(self):
        self.assertEqual(len(ShortUrl.objects.all()), 1)
        short_url = shortify(url=self.test_initial_url2)
        self.assertEqual(len(ShortUrl.objects.all()), 2)
        
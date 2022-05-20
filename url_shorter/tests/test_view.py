from django.test import TestCase
from django.urls import reverse
from django.test import Client

from url_shorter.models import ShortUrl
from url_shorter.services.api_urlshorter import shortify, BASE_SHORTER_URL


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.not_working_url = 'itshouldnotbeworking'
        self.url_shorter_url = reverse('urlshorter')
        self.url_shorter_api_url = reverse('api_urlshorter')
        self.initial_test_url = 'https://youtube.com/feed/subscriptions'
        self.initial_test_url_2 = 'https://www.dns-shop.ru/catalog/17a8932c16404e77/personalnye-kompyutery/'
        self.initial_test_url_3 = 'https://stackoverflow.com/questions/47020253/django-testing-how-to-assert-redirect'
        self.short_test_url = shortify(url=self.initial_test_url) # adding new ShortUrl object to db

    def test_url_shorter_get(self):

        response = self.client.get(self.url_shorter_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'url_shorter/urlshorter.html')

    def test_url_shorter_api_get(self):
        response = self.client.get(self.url_shorter_api_url, {'url': self.short_test_url})
        self.assertEqual(response.status_code, 200)
    
    def test_url_shorter_api_get_response(self):
        response = self.client.get(self.url_shorter_api_url, {
                                    'url': self.short_test_url}).json()
        obj = ShortUrl.objects.get(short_url=self.short_test_url)
        self.assertEqual(obj.initial_url,
                         response['initial_url'])
        short_url = BASE_SHORTER_URL + obj.short_url
        self.assertEqual(short_url,
                        response['short_url'])
        relative_url = '/l/' + obj.short_url
        self.assertEqual(relative_url,
                        response['relative_url'])
        self.assertEqual(self.initial_test_url, response['initial_url'])
    
    def test_url_shorter_api_get_failed(self):
        response = self.client.get(self.url_shorter_api_url, {
                                    'url': self.not_working_url}).json()
        self.assertEqual('failure', response['status'])
    

    def test_url_shorter_api_post(self):
        self.assertEqual(len(ShortUrl.objects.all()), 1)
        response = self.client.post(self.url_shorter_api_url, {
                                    'url': self.initial_test_url_2})
        self.assertEqual(len(ShortUrl.objects.all()), 2)
        self.assertEqual(ShortUrl.objects.last().initial_url,
                         self.initial_test_url_2)
        self.assertEqual(ShortUrl.objects.last().short_url,
                         shortify(url=self.initial_test_url_2))

    def test_url_already_exists(self):
        self.assertEqual(len(ShortUrl.objects.all()), 1)
        response = self.client.post(self.url_shorter_api_url, {
                                    'url': self.initial_test_url})
        self.assertEqual(len(ShortUrl.objects.all()), 1)

    def test_url_shorter_api_post_response(self):
        response = self.client.post(self.url_shorter_api_url, {
                                    'url': self.initial_test_url_3}).json()
        self.assertEqual(ShortUrl.objects.last().initial_url,
                         response['initial_url'])
        short_url = BASE_SHORTER_URL + ShortUrl.objects.last().short_url
        self.assertEqual(short_url,
                        response['short_url'])
        relative_url = '/l/' + ShortUrl.objects.last().short_url
        self.assertEqual(relative_url,
                        response['relative_url'])
        self.assertEqual(self.initial_test_url_3, response['initial_url'])
    
    def test_url_shorter_redirect(self):
        response = self.client.get(reverse('redir', kwargs={'url':self.short_test_url}))
        self.assertRedirects(response, self.initial_test_url, status_code=301, 
        target_status_code=200, fetch_redirect_response=False)
    
    def test_url_shorter_redirect_wrong_url(self):
        response = self.client.get(reverse('redir', kwargs={'url':self.not_working_url}))
        self.assertRedirects(response, f'http://{BASE_SHORTER_URL}', status_code=301, 
        target_status_code=200, fetch_redirect_response=False)
from http import client
from urllib import response
from django.test import TestCase
from django.urls import reverse
from django.test import Client

from url_shorter.models import ShortUrl


class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url_shorter_url = reverse('urlshorter')
        self.url_shorter_api_url = reverse('api_urlshorter')
    
    def test_url_shorter_get(self):
        
        response = self.client.get(self.url_shorter_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'url_shorter/urlshorter.html')
        
    def test_url_shorter_api_get(self):
        
        response = self.client.get(self.url_shorter_api_url)
        self.assertEqual(response.status_code, 200)
from django.urls import reverse, resolve
from django.test import SimpleTestCase
from ..views import UrlShorterAPI, UrlShorterView, ShorterRedirect

class TestUrls(SimpleTestCase):
    
    def test_urlshorter_url_resolves(self):
        url = reverse('urlshorter')
        self.assertEquals(resolve(url).func.view_class, UrlShorterView)
        
    
    def test_api_urlshorter_url_resolves(self):
        url = reverse('api_urlshorter')
        self.assertEquals(resolve(url).func.view_class, UrlShorterAPI)
    
    
    def test_redir_url_resolves(self):
        url = reverse('redir', kwargs={'url':'slug'})
        self.assertEquals(resolve(url).func.view_class, ShorterRedirect)

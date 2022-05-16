from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.http import HttpResponsePermanentRedirect
from .services.api_urlshorter import shortify, get_full_link, get_redirect_url, BASE_SHORTER_URL



class UrlShorterView(TemplateView):
    template_name = 'url_shorter/urlshorter.html'


class UrlShorterAPI(View):
    
    def get(self, request, *args, **kwargs):
        short_url = request.GET.get('url')
        url = get_full_link(short_url)
        if url:
            return JsonResponse({'status':'success',
                                'short_url': f'{BASE_SHORTER_URL}{short_url}',
                                'relative_url': f'/{short_url}',
                                'initial_url': f'{url.initial_url}'})
        return JsonResponse({'status': 'failure',
                            'error': f"Short url '{short_url}' does not exist"})
        
    def post(self, request, *args, **kwargs):
        url = request.POST['url']
        short_url = shortify(url=url)
        return JsonResponse({'status':'success',
                             'short_url': f'{BASE_SHORTER_URL}{short_url}',
                             'relative_url': f'/l/{short_url}',
                             'initial_url': f'{url}'
        })

class ShorterRedirect(View):
    
    def get(self, request, *args, **kwargs):
        url = get_redirect_url(self.kwargs['url'])
        return HttpResponsePermanentRedirect(redirect_to=url) 
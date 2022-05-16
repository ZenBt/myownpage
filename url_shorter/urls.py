from django.urls import path
from django.views.generic.base import RedirectView
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.UrlShorterView.as_view(), name='urlshorter'),
    path('api/', csrf_exempt(views.UrlShorterAPI.as_view()), name='api_urlshorter'),
    path('<url>', views.ShorterRedirect.as_view())
]

from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('article/<int:pk>', views.ArticleView.as_view(), name='article'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('projects', views.ProjectsView.as_view(), name='projects'),
    path('projects/<str:tag>', views.TagsView.as_view(), name='tags'),
    path('about', views.AboutView.as_view(), name='about'),
]

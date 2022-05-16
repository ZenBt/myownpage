from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.views import View

from .models import Article, Tag, Contact
from .forms import ContactForm


class IndexView(TemplateView):
    template_name = 'portfolio/index.html'
    

class ContactView(View, FormMixin):
    template_name = 'portfolio/contact.html'
    form_class = ContactForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_feedback = Contact(name=data['name'],
                                   surname=data['surname'],
                                   email=data['email'],
                                   topic=data['topic'],
                                   content=data['content'])
            new_feedback.save()
            return redirect('index')
        return render(request, self.template_name, {'form': form})


class AboutView(TemplateView):
    template_name = "portfolio/about.html"


class ArticleView(View):

    def get(self, request, *args, **kwargs):
        ctx = self.kwargs
        pk = ctx['pk']
        try:
            article = Article.objects.get(id=pk)
            tags = Tag.objects.filter(articles__pk=pk)
        except Article.DoesNotExist:
            return redirect('projects')
        return render(request, 'portfolio/article.html', {'article': article, 'tags': tags})


class ProjectsView(ListView):
    model = Article
    template_name = 'portfolio/projects.html'


class TagsView(ListView):
    template_name = 'portfolio/tags.html'

    def get_queryset(self):
        return Article.objects.filter(Tags__tag=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag')
        return context

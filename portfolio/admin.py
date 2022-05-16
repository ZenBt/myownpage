from django.contrib import admin
from .models import Article, Image, Tag, Contact

# Register your models here.
admin.site.register(Article)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(Contact)

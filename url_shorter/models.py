from django.db import models

class ShortUrl(models.Model):
    short_url = models.CharField(max_length=30)
    initial_url = models.CharField(max_length=400)

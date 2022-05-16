from django.db import models



class Contact(models.Model):
    name = models.CharField(max_length=30, null=True)
    surname = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=50)
    topic = models.CharField(max_length=120)
    content = models.TextField()

    def __str__(self):
        return self.email


class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    description = models.CharField(
        max_length=100, default='Описание недоступно')
    icon = models.ImageField(
        upload_to='uploads/', blank=True, null=True, default='uploads/missing-logo.png')
    header_pic = models.ImageField(upload_to='uploads/', blank=True, null=True)
    git_url = models.CharField(
        max_length=100, default='https://github.com/ZenBt/')
    review_url = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    tag = models.CharField(max_length=30)
    articles = models.ManyToManyField(Article, related_name='Tags')

    def __str__(self):
        return self.tag


class Image(models.Model):
    img = models.ImageField(upload_to='uploads/')
    post = models.ForeignKey(Article, on_delete=models.PROTECT)


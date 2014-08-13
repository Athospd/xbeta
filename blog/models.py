from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=40, unique=True, blank=True, null=True)

    def save(self):
        if not self.slug:
            self.slug = slugify(unicode(self.name))
        super(Category, self).save()

    def get_absolute_url(self):
        return "/category/%s/" % (self.slug)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class Tag(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=40, unique=True, blank=True, null=True)

    def save(self):
        if not self.slug:
            self.slug = slugify(unicode(self.name))
        super(Tag, self).save()

    def get_absolute_url(self):
        return "/tag/%s/" % (self.slug)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    pub_data = models.DateTimeField()
    texto = models.TextField()
    slug = models.SlugField(max_length=40, unique=True)
    author = models.ForeignKey(User)
    site = models.ForeignKey(Site)
    category = models.ForeignKey(Category, blank=True, null=True)
    tags = models.ManyToManyField(Tag)

    def get_absolute_url(self):
        return "/%s/%s/%s/" % (self.pub_data.year, self.pub_data.month, self.slug)

    def __unicode__(self):
        return self.titulo

    class Meta:
        ordering = ["-pub_data"]


from django.db import models


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    pub_data = models.DateTimeField()
    texto = models.TextField()
    slug = models.SlugField(max_length=40, unique=True)

    def get_absolute_url(self):
        return "/%s/%s/%s/" % (self.pub_data.year, self.pub_data.month, self.slug)

    def __unicode__(self):
        return self.titulo

    class Meta:
        ordering = ["-pub_data"]


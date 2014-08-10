from django.db import models


class Post(models.Model):
    titulo = models.CharField(max_length=200)
    pub_data = models.DateTimeField()
    texto = models.TextField()



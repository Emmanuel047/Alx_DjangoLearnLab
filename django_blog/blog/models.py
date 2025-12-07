from django.db import models

# Create your models here.
class Post(models.Models):
    title = models.CharFiield(max_lenght=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey

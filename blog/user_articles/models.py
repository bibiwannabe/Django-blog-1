from django.db import models
from tinymce.models import HTMLField

class Artical(models.Model):
    title = models.CharField(max_length=40)
    content = HTMLField()
    click = models.IntegerField()
    createdate = models.DateTimeField(auto_now_add=True)
    modifydate = models.DateTimeField(auto_now=True)
    uid = models.ForeignKey('user.UserInfo')
    def __str__(self):
        return self.title
# Create your models here.

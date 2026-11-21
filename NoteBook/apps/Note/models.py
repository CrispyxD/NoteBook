from django.db import models
from django.conf import settings
from apps.NoteCategory.models import CateogryModel

# Create your models here.
class NoteModel(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255,default="Unknown")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(CateogryModel,on_delete=models.SET_NULL,blank=True,null=True)
    Text = models.TextField()
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.author}"
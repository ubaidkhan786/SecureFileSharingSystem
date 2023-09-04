from django.db import models

# Create your models here.
class FileShare(models.Model):
    file_meta = models.FileField(upload_to = 'uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    #uploaded_by = models.CharField(max_length=200)
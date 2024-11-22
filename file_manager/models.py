from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        self.file_type = self.file.name.split('.')[-1].lower()
        super().save(*args, **kwargs)

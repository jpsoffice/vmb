from django.db import models
from tinymce import models as tinymce_models

# Create your models here.


class MailMessage(models.Model):
    title = models.CharField(max_length=100, null=True)
    message = tinymce_models.HTMLField()

    def __str__(self):
        return self.title

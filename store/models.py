from django.db import models

# Create your models here.

class Banner(models.Model):
        image1 = models.ImageField(upload_to='Banner')

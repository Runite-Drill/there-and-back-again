from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Destination(models.Model):
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    date = models.DateField()
    rating = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    comment = models.TextField(max_length=250)
    picture_upload = models.ImageField(default=None, blank=True, null=True, upload_to="main_app/static/images")
    picture_url = models.CharField(default='https://www.pngitem.com/pimgs/m/775-7750535_travel-globe-png-free-download-transparent-png.png', blank=True, null=True, max_length=100)
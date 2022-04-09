from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from .seed import COUNTRIES

# Create your models here.
CATEGORIES = (
    ('A', 'Activity'),
    ('C', 'Culture'),
    ('E', 'Event'),
    ('L', 'Landmark'),
    ('N', 'Nature'),
)


class Highlight(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=1, choices=CATEGORIES, default=CATEGORIES[0][0])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('highlights_index')
   
class Country(models.Model):
    name = models.CharField(max_length = 100, choices=COUNTRIES, default=COUNTRIES[0][0])
    picture_url = models.CharField(default='https://www.pngitem.com/pimgs/m/775-7750535_travel-globe-png-free-download-transparent-png.png', blank=True, null=True, max_length=100)
    highlights = models.ManyToManyField(Highlight)

    def get_absolute_url(self):
        return reverse('detail', kwargs = {'country_id':self.id})


class Review(models.Model):
    location = models.CharField(max_length=100)
    date_visited = models.DateField()
    rating = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    comment = models.TextField(max_length=250)
    picture = models.CharField(default='https://mir-s3-cdn-cf.behance.net/projects/max_808/8dd5b929789141.Y3JvcCw1MzIsNDE2LDAsMA.png', blank=True, null=True, max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    class Meta:
        ordering = ['-date_visited'] #sorts by date: ascending / (-) descending

    def get_absolute_url(self):
        return reverse('detail', kwargs = {'country_id':self.country.id})
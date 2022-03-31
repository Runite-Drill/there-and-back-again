from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

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
        return reverse('highlights_detail', kwargs = {'pk':self.id})
   
class Country(models.Model):
    country = models.CharField(max_length=100)
    date = models.DateField()
    rating = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    comment = models.TextField(max_length=250)
    picture_upload = models.ImageField(default=None, blank=True, null=True, upload_to="main_app/static/images")
    picture_url = models.CharField(default='https://www.pngitem.com/pimgs/m/775-7750535_travel-globe-png-free-download-transparent-png.png', blank=True, null=True, max_length=100)
    highlights = models.ManyToManyField(Highlight)

    def __str__(self):
        return self.name 

    def get_absolute_url(self):
        return reverse('detail', kwargs = {'country_id':self.id})


class Location(models.Model):
    location = models.CharField(max_length=100)
    date_visited = models.DateField()
    rating = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    comment = models.TextField(max_length=250)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_location_display()} on {self.date}"

    class Meta:
        ordering = ['-date_visited'] #sorts by date: ascending / (-) descending

 

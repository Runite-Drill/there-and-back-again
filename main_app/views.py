from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Country, Highlight
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import LocationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class countryCreate(LoginRequiredMixin, CreateView):
    model = Country
    fields = ['country','date','rating','comment','picture_upload','picture_url']

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form) #calls form_valid in parent class

class countryUpdate(LoginRequiredMixin, UpdateView):
    model = Country
    fields = ['date','rating','comment']

class countryDelete(LoginRequiredMixin, DeleteView):
    model = Country
    success_url = '/countries/'

#REPURPOSE THIS APP INTO A COUNTRY REVIEW TOOL?
#MANY USERS CAN RATE AND REVIEW AND LEAVE HIGHLIGHTS FOR COUNTRIES THEY HAVE VISITED
#USERS CAN THEN ALSO LOG THEIR TRAVEL TO THAT COUNTRY (VISIBLE ONLY TO THEM)

# class Destination:
#     def __init__(self, location, country, date, rating, comment):
#         self.location = location
#         self.country = country
#         self.date = date
#         self.rating = rating
#         self.comment = comment

'''
countries = [
    Destination('Queenstown','New Zealand','11-11-2015',6,'Lots of tourists.'),
    Destination('Vancouver','Canada','01-09-2014',7,'Exciting!'),
    Destination('Melbourne','Australia','10-01-2009',8,'Vibrant.'),
    Destination('Amsterdam','The Netherlands','01-07-2017',7,'Classic.'),
    Destination('Los Angeles','United States of America','01-09-2013',4,'Absolutely huge.'),
    Destination('Paris','France','10-07-2017',3,'Stinky and snobby.'),
    Destination('Rarotonga','Cook Islands','05-07-2009',6,'A peaceful beach escape, but not much else to do.'),
    Destination('Sydney','Australia','04-01-2009',4,'Nice bridge and opera house.'),
    Destination('Lima','Peru','21-02-2019',6,'Uniquely different.'),
    Destination('Geneva','Switzerland','20-07-2017',5,'Fascinating. Beautiful scenery.'),
    Destination('San Diego','United States of America','08-09-2013',5,'I only saw the zoo.'),
    Destination('Stockholm','Sweden','18-06-2019',7,'Charming European city!'),
    Destination('Buenos Aires','Argentina','24-03-2019',7,'Impressive city with great style.'),
    Destination('Brisbane','Australia','18-04-2019',6,'Pretty cool!'),
    Destination('Barcelona','Spain','25-06-2019',6,'It\'s got cool culture.'),
    Destination('Phoenix','United States of America','20-09-2013',3,'It didn\'t resonate with me.'),
    Destination('Auckland','New Zealand','01-01-2005',4,'It\'s kind of bland. Better to go to almost anywhere else in New Zealand.'),
    Destination('Rio de Janeiro','Brazil','26-03-2019',6,'Woah. Wild!'),
    Destination('Lisbon','Portugal','10-06-2019',7,'Culturally fascinating!'),
    Destination('Banff','Canada','22-09-2014',9,'This place is magical.'),
    Destination('Rome','Italy','01-01-2012',7,'Inspiring. Incredible!'),
    Destination('Venice','Italy','17-07-2017',4,'Kind of overrated.'),
    Destination('Florence','Italy','16-07-2017',5,'Also overrated. Unless you like art. Lots of art.'),
    Destination('Salzburg','Austria','18-07-2017',7,'This place is pretty cool.'),
    Destination('Stuttgart','Germany','27-06-2019',4,'Nothing special.'),
    Destination('Vatican City','Vatican City','01-01-2012',6,'Very impressive structure.'),
    Destination('Las Vegas','United States of America','15-09-2013',4,'$_$'),
    Destination('La Paz','Bolivia','16-03-2019',7,'Really enjoyed getting to know this place.'),
]
'''

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html') #render is the same as res.render in express

@login_required
def country_index(request):
    countries = Country.objects.filter(user = request.user)
    for i, country in enumerate(countries):
        if country.picture_upload != '':
            if country.picture_upload.name[:8] == "main_app":
                countries[i].picture_upload.name = '/' + country.picture_upload.name[9:]
            countries[i].picture = countries[i].picture_upload
        elif country.picture_url is not None:
            countries[i].picture = countries[i].picture_url

    return render(request, 'countries/index.html', {'countries':countries}) #can pass data into html file

@login_required
def country_detail(request,country_id):
    country = Country.objects.get(id=country_id)

    highlights_country_doesnt_have = Highlight.objects.exclude(id__in=country.highlights.all().values_list("id"))
    
    if country.picture_upload != '':
        if country.picture_upload.name[:8] == "main_app":
            country.picture_upload.name = '/' + country.picture_upload.name[9:]
        country.picture = country.picture_upload
    elif country.picture_url is not None:
        country.picture = country.picture_url
    else:
        country.picture = None

    location_form = LocationForm()
    return render(request, 'countries/detail.html', {'country':country, 'location_form':location_form,'highlights':highlights_country_doesnt_have})


@login_required
def add_location(request,country_id):
    form = LocationForm(request.POST)
    if form.is_valid():
        new_location = form.save(commit=False)
        new_location.country_id = country_id
        new_location.save()
    return redirect('detail', country_id=country_id)

#TOY CRUD
class highlightList(LoginRequiredMixin, ListView):
    model = Highlight

class highlightDetail(LoginRequiredMixin, DetailView):
    model = Highlight

class highlightCreate(LoginRequiredMixin, CreateView):
    model = Highlight
    fields = '__all__'

class highlightUpdate(LoginRequiredMixin, UpdateView):
    model = Highlight
    fields = '__all__'

class highlightDelete(LoginRequiredMixin, DeleteView):
    model = Highlight
    success_url = '/highlights/'

@login_required
def assoc_highlight(request, country_id, highlight_id):
    Country.objects.get(id=country_id).highlights.add(highlight_id)
    return redirect('detail', country_id=country_id)

@login_required
def unassoc_highlight(request, country_id, highlight_id):
    Country.objects.get(id=country_id).highlights.remove(highlight_id)
    return redirect('detail', country_id=country_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() #save the user to the database
            login(request, user) #login the user
            return redirect('index')
        else:
            error_message = 'Invalid signup - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

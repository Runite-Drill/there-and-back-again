from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Country, Highlight, Review
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import ReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .seed import COUNTRIES

# Create your views here.
class countryCreate(LoginRequiredMixin, CreateView):
    model = Country
    fields = ['country','date','rating','comment','picture_upload','picture_url']

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form) #calls form_valid in parent class

class reviewUpdate(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['date_visited', 'location', 'rating', 'comment', 'picture']

class reviewDelete(LoginRequiredMixin, DeleteView):
    model = Review
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


def home(request):
    countries = Country.objects.all()
    if len(countries) == 0:
        for elem in COUNTRIES:
            Country.objects.create(name=elem[0], picture_url='https://www.pngitem.com/pimgs/m/775-7750535_travel-globe-png-free-download-transparent-png.png')
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html') #render is the same as res.render in express

def country_index(request):
    # countries = Country.objects.filter(user = request.user)
    countries = Country.objects.all()
    for country in countries:
        reviews = Review.objects.filter(country=country)
        rating = 0;
        country.rating = 0;
        if len(reviews) > 0:
            for review in reviews:
                rating+=review.rating
            rating = rating/len(reviews)
            country.rating = round(rating,2)


    return render(request, 'countries/index.html', {'countries':countries}) #can pass data into html file

def country_detail(request,country_id):
    country = Country.objects.get(id=country_id)
    # reviews = Review.objects.filter(user=request.user, country=country)
    # print(reviews[0].comment)
    highlights_country_doesnt_have = Highlight.objects.exclude(id__in=country.highlights.all().values_list("id"))

    review_form = ReviewForm()
    return render(request, 'countries/detail.html', {'country':country, 'review_form':review_form,'highlights':highlights_country_doesnt_have})


@login_required
def add_review(request,country_id):
    form = ReviewForm(request.POST)
    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.country_id = country_id
        new_review.user_id = request.user.id
        new_review.save()
    return redirect('detail', country_id=country_id)

class reviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    fields = '__all__'

#TOY CRUD
class highlightList(ListView):
    model = Highlight

class highlightDetail(DetailView):
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

from django.urls import path
from . import views
urlpatterns = [
    path("",views.home, name="home"), #mount the home view on the root path and name the url "home"
    path("about/",views.about, name="about"),
    path("countries/",views.country_index, name="index"),
    path("countries/<int:country_id>/",views.country_detail, name="detail"),
    path("countries/create/",views.countryCreate.as_view(), name="country_create"),
    path("countries/<int:pk>/update/",views.countryUpdate.as_view(), name="country_update"),
    path("countries/<int:pk>/delete/",views.countryDelete.as_view(), name="country_delete"), 
    path('countries/<int:country_id>/add_location/', views.add_location, name="add_location")
]
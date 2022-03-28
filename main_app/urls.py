from django.urls import path
from . import views
urlpatterns = [
    path("",views.home, name="home"), #mount the home view on the root path and name the url "home"
    path("about/",views.about, name="about"),
    path("destinations/",views.destination_index, name="index"),
    path("destinations/<int:destination_id>/",views.destination_detail, name="detail"),
]
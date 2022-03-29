from django.urls import path
from . import views
urlpatterns = [
    path("",views.home, name="home"), #mount the home view on the root path and name the url "home"
    path("about/",views.about, name="about"),
    path("destinations/",views.destination_index, name="index"),
    path("destinations/<int:destination_id>/",views.destination_detail, name="detail"),
    path("destinations/create/",views.destinationCreate.as_view(), name="destination_create"),
    path("destinations/<int:pk>/update/",views.destinationUpdate.as_view(), name="destination_update"),
    path("destinations/<int:pk>/delete/",views.destinationDelete.as_view(), name="destination_delete"), 
    path('destinations/<int:destination_id>/add_location/', views.add_location, name="add_location")
]
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
    path('countries/<int:country_id>/add_location/', views.add_location, name="add_location"),

    #HIGHLIGHTS CRUD
    path("highlights/",views.highlightList.as_view(), name="highlights_index"),
    path("highlights/<int:pk>/",views.highlightDetail.as_view(), name="highlights_detail"),
    path("highlights/create/",views.highlightCreate.as_view(), name="highlights_create"),
    path("highlights/<int:pk>/update/",views.highlightUpdate.as_view(), name="highlights_update"),
    path("highlights/<int:pk>/delete",views.highlightDelete.as_view(), name="highlights_delete"),

    #associate hightlight with country
    path('countries/<int:country_id>/assoc_highlight/<int:highlight_id>/', views.assoc_highlight, name = 'assoc_highlight'),
    path('countries/<int:country_id>/unassoc_highlight/<int:highlight_id>/', views.unassoc_highlight, name = 'unassoc_highlight'),
    
    #URL for signup
    path('accounts/signup/', views.signup, name="signup")
]
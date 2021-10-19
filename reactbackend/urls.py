from django.urls import path
from . import views



urlpatterns = [
    path("", views.get_categories),
    path("get_categories", views.get_categories, name="react_get_categories"),
 
]


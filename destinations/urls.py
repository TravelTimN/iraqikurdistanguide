from django.urls import path
from . import views

urlpatterns = [
    path("", views.destinations, name="destinations"),
    path("add/", views.add_destination, name="add_destination"),
    path("update/", views.update_destination, name="update_destination"),
]

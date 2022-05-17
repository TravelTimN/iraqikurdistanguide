from django.urls import path
from . import views

urlpatterns = [
    path("", views.destinations, name="destinations"),
    path("<int:id>/", views.destination, name="destination"),
    path("add/", views.add_destination, name="add_destination"),
    path("update/<int:id>", views.update_destination, name="update_destination"),
]

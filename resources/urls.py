from django.urls import path
from . import views

urlpatterns = [
    path("", views.resources, name="resources"),
    path("alphabet/", views.alphabet, name="alphabet"),
    path("phrases/", views.phrases, name="phrases"),
    path("phrases/add/", views.add_phrase, name="add_phrase"),
    path("phrases/update/<int:id>", views.update_phrase, name="update_phrase"),
    path("phrases/delete/<int:id>", views.delete_phrase, name="delete_phrase"),
    path("weather/", views.weather, name="weather"),
]

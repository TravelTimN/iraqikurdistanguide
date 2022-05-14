from django.urls import path
from . import views

urlpatterns = [
    path("", views.resources, name="resources"),
    path("alphabet/", views.alphabet, name="alphabet"),
    path("phrases/", views.phrases, name="phrases"),
]

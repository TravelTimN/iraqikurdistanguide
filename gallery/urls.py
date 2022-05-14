from django.urls import path
from . import views

urlpatterns = [
    path("", views.gallery, name="gallery"),
    path("add/", views.add_image, name="add_image"),
    path("update/", views.update_image, name="update_image"),
]

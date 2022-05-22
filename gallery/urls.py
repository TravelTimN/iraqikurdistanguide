from django.urls import path
from . import views

urlpatterns = [
    path("", views.gallery, name="gallery"),
    path("add/", views.add_photo, name="add_photo"),
    path("update/<int:id>", views.update_photo, name="update_photo"),
    path("delete/<int:id>", views.delete_photo, name="delete_photo"),
]

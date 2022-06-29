from django.urls import path
from . import views

urlpatterns = [
    path("", views.reviews, name="reviews"),
    path("add/", views.add_review, name="add_review"),
    path("update/<int:id>", views.update_review, name="update_review"),
    path("delete/<int:id>", views.delete_review, name="delete_review"),
]

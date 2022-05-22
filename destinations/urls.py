from django.urls import path
from . import views

urlpatterns = [
    path("", views.destinations, name="destinations"),
    path("add/", views.add_destination, name="add_destination"),
    path("view/<int:id>/", views.view_destination, name="view_destination"),
    path("update/<int:id>", views.update_destination, name="update_destination"),
    path("delete/<int:id>", views.delete_destination, name="delete_destination"),
    path("<int:id>/sight/add/", views.add_sight, name="add_sight"),
    path("<int:d_id>/sight/<int:s_id>", views.view_sight, name="view_sight"),
    path("<int:d_id>/sight/update/<int:s_id>", views.update_sight, name="update_sight"),
    path("<int:d_id>/sight/delete/<int:s_id>", views.delete_sight, name="delete_sight"),
]

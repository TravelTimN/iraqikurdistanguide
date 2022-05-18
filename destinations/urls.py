from django.urls import path
from . import views

urlpatterns = [
    path("", views.destinations, name="destinations"),
    path("add/", views.add_destination, name="add_destination"),
    path("view/<int:id>/", views.view_destination, name="view_destination"),
    path("update/<int:id>", views.update_destination, name="update_destination"),
    path("<int:id>/site/add/", views.add_site, name="add_site"),
    path("<int:d_id>/site/<int:s_id>", views.view_site, name="view_site"),
    path("<int:d_id>/site/update/<int:s_id>", views.update_site, name="update_site"),
]

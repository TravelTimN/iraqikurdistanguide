from django.urls import path
from . import views

urlpatterns = [
    path("", views.calendar_bookings, name="calendar_bookings"),
    path("all/", views.all_bookings, name="all_bookings"),
    path("add/", views.add_booking, name="add_booking"),
    path("update/<int:id>", views.update_booking, name="update_booking"),
    path("delete/<int:id>", views.delete_booking, name="delete_booking"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.itineraries, name="itineraries"),
    # itinerary
    path("add/", views.add_itinerary, name="add_itinerary"),
    path("update/<int:id>/", views.update_itinerary, name="update_itinerary"),  # noqa
    path("delete/<int:id>/", views.delete_itinerary, name="delete_itinerary"),
    # itinerary days
    path("add_day/<int:id>/", views.add_itinerary_day, name="add_itinerary_day"),  # noqa
    path("update_day/<int:itin_id>/<int:day_id>/", views.update_itinerary_day, name="update_itinerary_day"),  # noqa
    path("delete_day/<int:itin_id>/<int:day_id>/", views.delete_itinerary_day, name="delete_itinerary_day"),  # noqa
]

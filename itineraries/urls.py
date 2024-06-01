from django.urls import path
from . import views

urlpatterns = [
    path("", views.itineraries, name="itineraries"),
    # path("add/", views.add_faq, name="add_faq"),
    # path("update/<int:id>", views.update_faq, name="update_faq"),
    # path("delete/<int:id>", views.delete_faq, name="delete_faq"),
]

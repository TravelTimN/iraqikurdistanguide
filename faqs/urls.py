from django.urls import path
from . import views

urlpatterns = [
    path("", views.faqs, name="faqs"),
    path("add/", views.add_faq, name="add_faq"),
    path("update/", views.update_faq, name="update_faq"),
]
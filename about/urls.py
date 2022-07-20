from django.urls import path
from . import views

urlpatterns = [
    path("", views.about, name="about"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("terms_conditions/", views.terms_conditions, name="terms_conditions")
]

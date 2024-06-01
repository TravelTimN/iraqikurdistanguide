import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import handler400, handler403, handler404, handler500

urlpatterns = [
    path(f"{os.environ.get('ADMIN_URL')}/", admin.site.urls),
    path("profile/", include("accounts.urls")),
    path(f"{os.environ.get('AUTH_URL')}/", include("allauth.urls")),
    path("tinymce/", include("tinymce.urls")),
    path("", include("home.urls")),
    path("about/", include("about.urls")),
    path("bookings/", include("bookings.urls")),
    path("contact/", include("contact.urls")),
    path("destinations/", include("destinations.urls")),
    path("faqs/", include("faqs.urls")),
    path("gallery/", include("gallery.urls")),
    path("resources/", include("resources.urls")),
    path("reviews/", include("reviews.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = "main.views.handler400"
handler403 = "main.views.handler403"
handler404 = "main.views.handler404"
handler500 = "main.views.handler500"

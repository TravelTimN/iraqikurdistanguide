from django.conf import settings


# leaflet map api
def map_url_api(request):
    return {"map_url": settings.MAP_URL}

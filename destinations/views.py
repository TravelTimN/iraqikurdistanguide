from django.shortcuts import render
from django.conf import settings
from .models import Destination


def destinations(request):
    """ A view to return the destinations page """
    map_url = settings.MAP_URL
    destinations = Destination.objects.all()
    template = "destinations/destinations.html"
    context = {
        "map_url": map_url,
        "destinations": destinations,
    }
    return render(request, template, context)


def add_destination(request):
    """ A view to add a single destination """
    return render(request, "destinations/add_destination.html")


def update_destination(request):
    """ A view to update a specific destination """
    return render(request, "destinations/update_destination.html")

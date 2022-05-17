from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib import messages
from .models import Destination, Site


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


def destination(request, id):
    """ A view to return the destinations page """
    map_url = settings.MAP_URL
    destination = get_object_or_404(Destination, id=id)
    sites = Site.objects.filter(destination=destination)
    template = "destinations/destination.html"
    context = {
        "map_url": map_url,
        "destination": destination,
        "sites": sites,
    }
    return render(request, template, context)


def add_destination(request):
    """ A view to add a single destination """
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
    template = "destinations/add_destination.html"
    context = {}
    return render(request, template, context)


def update_destination(request, id):
    """ A view to update a specific destination """
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
    destination = get_object_or_404(Destination, id=id)
    template = "destinations/update_destination.html"
    context = {
        "destination": destination,
    }
    return render(request, template, context)

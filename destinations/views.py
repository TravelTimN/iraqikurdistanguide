from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib import messages
from .models import Destination, Site
from .forms import DestinationForm


MAP_URL = settings.MAP_URL


def destinations(request):
    """ A view to return the destinations page """
    destinations = Destination.objects.all()
    template = "destinations/destinations.html"
    context = {
        "map_url": MAP_URL,
        "destinations": destinations,
    }
    return render(request, template, context)


def add_destination(request):
    """ A view to add a single destination """
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
    destination_form = DestinationForm(request.POST or None)
    if request.method == "POST":
        if destination_form.is_valid():
            new_destination = destination_form.save()
            messages.success(request, "Destination Added!")
            return redirect(view_destination, new_destination.pk)
        messages.error(request, "Error: Please Try Again.")
    destination_form = DestinationForm()
    template = "destinations/add_destination.html"
    context = {
        "map_url": MAP_URL,
        "destination_form": destination_form,
    }
    return render(request, template, context)


def view_destination(request, id):
    """ A view to return the destination-specific page """
    destination = get_object_or_404(Destination, id=id)
    sites = Site.objects.filter(destination=destination)
    template = "destinations/view_destination.html"
    context = {
        "map_url": MAP_URL,
        "destination": destination,
        "sites": sites,
    }
    return render(request, template, context)


def update_destination(request, id):
    """ A view to update a specific destination """
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
    destination = get_object_or_404(Destination, id=id)
    destination_form = DestinationForm(request.POST or None, instance=destination)
    if request.method == "POST":
        if destination_form.is_valid():
            destination_form.save()
            messages.success(request, "Destination Updated!")
            return redirect(view_destination, id)
        messages.error(request, "Error: Please Try Again.")
    destination_form = DestinationForm(instance=destination)
    template = "destinations/update_destination.html"
    context = {
        "map_url": MAP_URL,
        "destination": destination,
        "destination_form": destination_form,
    }
    return render(request, template, context)


def add_site(request, id):
    """ A view to add a single site/POI """
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
    destination = get_object_or_404(Destination, id=id)
    template = "destinations/add_site.html"
    context = {
        "destination": destination,
    }
    return render(request, template, context)


def view_site(request, d_id, s_id):
    """ A view to return the site-specific page """
    destination = get_object_or_404(Destination, id=d_id)
    site = get_object_or_404(Site, id=s_id)
    template = "destinations/view_site.html"
    context = {
        "map_url": MAP_URL,
        "destination": destination,
        "site": site,
    }
    return render(request, template, context)


def update_site(request, d_id, s_id):
    """ A view to update a specific site """
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
    destination = get_object_or_404(Destination, id=d_id)
    site = get_object_or_404(Site, id=s_id)
    template = "destinations/update_site.html"
    context = {
        "destination": destination,
        "site": site,
    }
    return render(request, template, context)

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Destination, Sight, Tour
from .forms import DestinationForm, SightForm, TourForm
from gallery.models import Photo
from main.decorators import validate_user


MAP_URL = settings.MAP_URL


def destinations(request):
    """ A view to return the destinations page """
    if request.user.is_superuser:
        destinations = Destination.objects.all()
    else:
        destinations = Destination.objects.filter(is_visible=True)
    template = "destinations/destinations.html"
    context = {
        "map_url": MAP_URL,
        "destinations": destinations,
    }
    return render(request, template, context)


@validate_user()
def add_destination(request):
    """ A view to add a single destination """
    destination_form = DestinationForm(request.POST or None)
    if request.method == "POST":
        if destination_form.is_valid():
            next = request.POST.get("next", "/")
            new_destination = destination_form.save()
            messages.success(request, f"{new_destination.name} Added!")
            return HttpResponseRedirect(next)
        messages.error(request, "Error: Please Try Again.")
    template = "destinations/add_destination.html"
    context = {
        "map_url": MAP_URL,
        "destination_form": destination_form,
    }
    return render(request, template, context)


def view_destination(request, id):
    """ A view to return the destination-specific page """
    destination = get_object_or_404(Destination, id=id)
    if request.user.is_superuser:
        sights = Sight.objects.filter(destination=destination)
    else:
        sights = Sight.objects.filter(destination=destination, is_visible=True)
    template = "destinations/view_destination.html"
    context = {
        "map_url": MAP_URL,
        "destination": destination,
        "sights": sights,
    }
    return render(request, template, context)


@validate_user()
def update_destination(request, id):
    """ A view to update a specific destination """
    destination = get_object_or_404(Destination, id=id)
    destination_form = DestinationForm(request.POST or None, instance=destination)
    if request.method == "POST":
        if destination_form.is_valid():
            next = request.POST.get("next", "/")
            updated_destination = destination_form.save()
            messages.success(request, f"{updated_destination.name} Updated!")
            return HttpResponseRedirect(next)
        messages.error(request, "Error: Please Try Again.")
    destination_form = DestinationForm(instance=destination)
    template = "destinations/update_destination.html"
    context = {
        "map_url": MAP_URL,
        "destination": destination,
        "destination_form": destination_form,
    }
    return render(request, template, context)


@validate_user()
def delete_destination(request, id):
    """ A view to delete a single destination """
    destination = get_object_or_404(Destination, id=id)
    messages.success(request, f"{destination.name} Deleted!")
    destination.delete()
    return redirect(reverse("destinations"))


@validate_user()
def add_sight(request, id):
    """ A view to add a single sight/POI """
    destination = get_object_or_404(Destination, id=id)
    sight_form = SightForm(request.POST or None, initial={"destination": id})
    if request.method == "POST":
        if sight_form.is_valid():
            next = request.POST.get("next", "/")
            new_sight = sight_form.save()
            messages.success(request, f"{new_sight.name} Added!")
            return HttpResponseRedirect(next)
        messages.error(request, "Error: Please Try Again.")
    template = "destinations/add_sight.html"
    context = {
        "map_url": MAP_URL,
        "destination": destination,
        "sight_form": sight_form,
    }
    return render(request, template, context)


def view_sight(request, d_id, s_id):
    """ A view to return the sight-specific page """
    destination = get_object_or_404(Destination, id=d_id)
    sight = get_object_or_404(Sight, id=s_id)
    if request.user.is_superuser:
        photo_group = Photo.objects.filter(sight=sight)
    else:
        photo_group = Photo.objects.filter(sight=sight, is_visible=True)
    template = "destinations/view_sight.html"
    context = {
        "map_url": MAP_URL,
        "destination": destination,
        "sight": sight,
        "photo_group": photo_group,
    }
    return render(request, template, context)


@validate_user()
def update_sight(request, d_id, s_id):
    """ A view to update a specific sight """
    destination = get_object_or_404(Destination, id=d_id)
    sight = get_object_or_404(Sight, id=s_id)
    sight_form = SightForm(request.POST or None, instance=sight)
    if request.method == "POST":
        if sight_form.is_valid():
            next = request.POST.get("next", "/")
            updated_sight = sight_form.save()
            messages.success(request, f"{updated_sight.name} Updated!")
            return HttpResponseRedirect(next)
        messages.error(request, "Error: Please Try Again.")
    sight_form = SightForm(instance=sight)
    template = "destinations/update_sight.html"
    context = {
        "map_url": MAP_URL,
        "destination": destination,
        "sight": sight,
        "sight_form": sight_form,
    }
    return render(request, template, context)


@validate_user()
def delete_sight(request, d_id, s_id):
    """ A view to delete a single sight """
    sight = get_object_or_404(Sight, id=s_id)
    messages.success(request, f"{sight.name} Deleted!")
    sight.delete()
    return redirect(reverse("destinations"))


@validate_user()
def add_tour(request):
    """ A view to add a single tour """
    tour_form = TourForm(request.POST or None)
    if request.method == "POST":
        if tour_form.is_valid():
            tour_form.save()
            messages.success(request, "Tour Added!")
            return redirect(reverse("home") + "#tours")
        messages.error(request, "Error: Please Try Again.")
    template = "destinations/add_tour.html"
    context = {
        "tour_form": tour_form,
    }
    return render(request, template, context)


@validate_user()
def update_tour(request, id):
    """ A view to update a specific tour """
    tour = get_object_or_404(Tour, id=id)
    tour_form = TourForm(request.POST or None, instance=tour)
    if request.method == "POST":
        if tour_form.is_valid():
            tour_form.save()
            messages.success(request, f"{tour.category} Updated!")
            return redirect(reverse("home") + "#tours")
        messages.error(request, "Error: Please Try Again.")
    tour_form = TourForm(instance=tour)
    template = "destinations/update_tour.html"
    context = {
        "tour": tour,
        "tour_form": tour_form,
    }
    return render(request, template, context)


@validate_user()
def delete_tour(request, id):
    """ A view to delete a single tour """
    tour = get_object_or_404(Tour, id=id)
    messages.success(request, f"{tour.category} Deleted!")
    tour.delete()
    return redirect(reverse("home") + "#tours")

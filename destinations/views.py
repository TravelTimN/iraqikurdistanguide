from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Destination, Sight
from .forms import DestinationForm, SightForm


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


@login_required
def add_destination(request):
    """ A view to add a single destination """
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
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


@login_required
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


@login_required
def delete_destination(request, id):
    """ A view to delete a single destination """
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
    destination = get_object_or_404(Destination, id=id)
    messages.success(request, f"{destination.name} Deleted!")
    destination.delete()
    return redirect(reverse("destinations"))


def add_sight(request, id):
    """ A view to add a single sight/POI """
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
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
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
    destination = get_object_or_404(Destination, id=d_id)
    sight = get_object_or_404(Sight, id=s_id)
    template = "destinations/view_sight.html"
    context = {
        "map_url": MAP_URL,
        "destination": destination,
        "sight": sight,
    }
    return render(request, template, context)


def update_sight(request, d_id, s_id):
    """ A view to update a specific sight """
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
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


def delete_sight(request, d_id, s_id):
    """ A view to delete a single sight """
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
    sight = get_object_or_404(Sight, id=s_id)
    messages.success(request, f"{sight.name} Deleted!")
    sight.delete()
    return redirect(reverse("destinations"))

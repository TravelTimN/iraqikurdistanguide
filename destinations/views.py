from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Destination, Site
from .forms import DestinationForm, SiteForm


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
        sites = Site.objects.filter(destination=destination)
    else:
        sites = Site.objects.filter(destination=destination, is_visible=True)
    template = "destinations/view_destination.html"
    context = {
        "map_url": MAP_URL,
        "destination": destination,
        "sites": sites,
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


@login_required
def add_site(request, id):
    """ A view to add a single site/POI """
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
    destination = get_object_or_404(Destination, id=id)
    site_form = SiteForm(request.POST or None, initial={"destination": id})
    if request.method == "POST":
        if site_form.is_valid():
            next = request.POST.get("next", "/")
            new_site = site_form.save()
            messages.success(request, f"{new_site.name} Added!")
            return HttpResponseRedirect(next)
        messages.error(request, "Error: Please Try Again.")
    template = "destinations/add_site.html"
    context = {
        "map_url": MAP_URL,
        "destination": destination,
        "site_form": site_form,
    }
    return render(request, template, context)


def view_site(request, d_id, s_id):
    """ A view to return the site-specific page """
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
    destination = get_object_or_404(Destination, id=d_id)
    site = get_object_or_404(Site, id=s_id)
    template = "destinations/view_site.html"
    context = {
        "map_url": MAP_URL,
        "destination": destination,
        "site": site,
    }
    return render(request, template, context)


@login_required
def update_site(request, d_id, s_id):
    """ A view to update a specific site """
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
    destination = get_object_or_404(Destination, id=d_id)
    site = get_object_or_404(Site, id=s_id)
    site_form = SiteForm(request.POST or None, instance=site)
    if request.method == "POST":
        if site_form.is_valid():
            next = request.POST.get("next", "/")
            updated_site = site_form.save()
            messages.success(request, f"{updated_site.name} Updated!")
            return HttpResponseRedirect(next)
        messages.error(request, "Error: Please Try Again.")
    site_form = SiteForm(instance=site)
    template = "destinations/update_site.html"
    context = {
        "map_url": MAP_URL,
        "destination": destination,
        "site": site,
        "site_form": site_form,
    }
    return render(request, template, context)


@login_required
def delete_site(request, d_id, s_id):
    """ A view to delete a single site """
    if not request.user.is_superuser:
        # user is not superuser; take them to all destinations
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("destinations"))
    site = get_object_or_404(Site, id=s_id)
    messages.success(request, f"{site.name} Deleted!")
    site.delete()
    return redirect(reverse("destinations"))

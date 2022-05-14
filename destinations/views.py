from django.shortcuts import render


def destinations(request):
    """ A view to return the destinations page """
    return render(request, "destinations/destinations.html")


def add_destination(request):
    """ A view to add a single destination """
    return render(request, "destinations/add_destination.html")


def update_destination(request):
    """ A view to update a specific destination """
    return render(request, "destinations/update_destination.html")

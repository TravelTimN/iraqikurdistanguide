from django.shortcuts import render
from destinations.models import Destination, Tour


def about(request):
    """ A view to return the about page """
    if request.user.groups.filter(name="Site Admin"):
        destinations = Destination.objects.all()
        tours = Tour.objects.all()
    else:
        destinations = Destination.objects.filter(is_visible=True)
        tours = Tour.objects.filter(is_visible=True)
    template = "about/about.html"
    context = {
        "destinations": destinations,
        "tours": tours,
    }
    return render(request, template, context)


def privacy_policy(request):
    """ A view to return the Privacy Policy page """
    return render(request, "about/privacy_policy.html")


def terms_conditions(request):
    """ A view to return the Terms & Conditions page """
    return render(request, "about/terms_conditions.html")

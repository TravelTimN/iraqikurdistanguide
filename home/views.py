from django.shortcuts import render
from destinations.models import Tour


def home(request):
    """ A view to return the home page """
    if request.user.is_superuser:
        tours = Tour.objects.all()
    else:
        tours = Tour.objects.filter(is_visible=True)
    template = "home/index.html"
    context = {
        "tours": tours,
    }
    return render(request, template, context)

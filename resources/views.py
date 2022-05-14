from django.shortcuts import render


def resources(request):
    """ A view to return the resources page """
    return render(request, "resources/resources.html")


def alphabet(request):
    """ A view to return the alphabet page """
    return render(request, "resources/alphabet.html")


def phrases(request):
    """ A view to return the phrases page """
    return render(request, "resources/phrases.html")

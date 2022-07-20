from django.shortcuts import render


def about(request):
    """ A view to return the about page """
    return render(request, "about/about.html")


def privacy_policy(request):
    """ A view to return the Privacy Policy page """
    return render(request, "about/privacy_policy.html")


def terms_conditions(request):
    """ A view to return the Terms & Conditions page """
    return render(request, "about/terms_conditions.html")

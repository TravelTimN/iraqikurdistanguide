from django.shortcuts import render
from .models import FAQ


def faqs(request):
    """ A view to return the FAQs page """
    if request.user.is_superuser:
        faqs = FAQ.objects.all().order_by("category")
    else:
        faqs = FAQ.objects.filter(is_visible=True).order_by("category")
    template = "faqs/faqs.html"
    context = {
        "faqs": faqs,
    }
    return render(request, template, context)


def add_faq(request):
    """ A view to add a new FAQ """
    return render(request, "faqs/add_faq.html")


def update_faq(request):
    """ A view to update a specific FAQ """
    return render(request, "faqs/update_faq.html")

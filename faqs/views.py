from django.shortcuts import render


def faqs(request):
    """ A view to return the FAQs page """
    return render(request, "faqs/faqs.html")


def add_faq(request):
    """ A view to add a new FAQ """
    return render(request, "faqs/add_faq.html")


def update_faq(request):
    """ A view to update a specific FAQ """
    return render(request, "faqs/update_faq.html")

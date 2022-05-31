from django.shortcuts import render, redirect, reverse
from .models import Contact
from .forms import ContactForm
from django.contrib import messages


def contact(request):
    """ A view to return the contact page """
    contact_form = ContactForm(request.POST or None)
    if request.method == "POST":
        if contact_form.is_valid:
            contact_form.save()
            messages.success(request, "Message sent!")
            return redirect(reverse("contact"))
    template = "contact/contact.html"
    context = {
        "contact_form": contact_form,
    }
    return render(request, template, context)

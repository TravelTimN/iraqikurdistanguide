import datetime
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Contact
from .forms import ContactForm
from destinations.models import Destination


def contact(request):
    """ A view to return the contact page """
    contact_form = ContactForm(request.POST or None)
    if request.method == "POST":
        if contact_form.is_valid():
            contact_form.save()
            messages.success(
                request,
                "Thank You! We'll be in touch with you soon!"
            )

            # generate list of wishlist destinations
            destinations = []
            for destination in request.POST.getlist("destinations"):
                if isinstance(int(destination), int):
                    location = get_object_or_404(Destination, id=int(destination))
                    destinations.append(location.name)

            # form data collection
            form_context = {
                "name": request.POST.get("name"),
                "email": request.POST.get("email"),
                "phone_num": request.POST.get("phone_num"),
                "start_date": datetime.datetime.strftime(datetime.datetime.strptime(request.POST.get("start_date"), "%Y-%m-%d"), "%d %B, %Y"),  # noqa
                "end_date": datetime.datetime.strftime(datetime.datetime.strptime(request.POST.get("start_date"), "%Y-%m-%d") + datetime.timedelta(int(request.POST.get("num_days"))), "%d %B, %Y"),  # noqa
                "num_days": request.POST.get("num_days"),
                "num_guests": request.POST.get("num_guests"),
                "message": request.POST.get("message"),
                "destinations": ", ".join(destinations),
            }

            # send email
            send_mail(
                "New Trip Request (Iraqi Kurdistan Guide)",
                render_to_string(
                    "contact/emails/trip_request.txt",
                    {"form_context": form_context}
                ),
                settings.DEFAULT_FROM_EMAIL,
                # [settings.DEFAULT_OWNER_EMAIL],  # TODO: link to Haval
                [settings.DEFAULT_FROM_EMAIL],  # TODO: remove this
            )

            return redirect(reverse("home"))
    template = "contact/contact.html"
    context = {
        "contact_form": contact_form,
    }
    return render(request, template, context)

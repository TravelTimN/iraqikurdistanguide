from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives, BadHeaderError
from django.template.loader import render_to_string
from django_countries.fields import Country
from .models import Contact
from .forms import ContactForm
from bookings.models import Booking
from destinations.models import Destination


def contact(request):
    """ A view to return the contact page """
    contact_form = ContactForm(request.POST or None)
    if request.method == "POST":
        if contact_form.is_valid():
            new_contact = contact_form.save()

            # generate list of wishlist destinations
            destinations = []
            for destination in request.POST.getlist("destinations"):
                if destination.isdigit():
                    location = get_object_or_404(Destination, id=int(destination))
                    destinations.append(location)

            # create new Booking object
            start_date = datetime.strptime(request.POST.get("start_date"), "%Y-%m-%d")
            end_date = start_date + timedelta(int(request.POST.get("num_days")))
            booking = Booking.objects.create(
                guide="haval",
                guest_name=request.POST.get("name"),
                guest_email=request.POST.get("email"),
                guest_phone=request.POST.get("phone_num"),
                guest_country=request.POST.get("country"),
                total_guests=request.POST.get("num_guests"),
                start_date=start_date,
                end_date=end_date,
                currency="usd",
                total_price=0,
                amount_paid=0,
                status="new",
                contact_message=new_contact,
                notes=request.POST.get("message"),
            )
            booking.itinerary.set(destinations)
            booking_id = booking.id

            # get country name from country code
            country_code = request.POST.get("country")
            country_name = Country(code=country_code).name

            # form data collection for email
            form_context = {
                "id": booking_id,
                "name": request.POST.get("name"),
                "email": request.POST.get("email"),
                "phone_num": request.POST.get("phone_num"),
                "country": country_name,
                "start_date": datetime.strptime(request.POST.get("start_date"), "%Y-%m-%d").strftime("%d %B, %Y"),  # noqa
                "end_date": (datetime.strptime(request.POST.get("start_date"), "%Y-%m-%d") + timedelta(int(request.POST.get("num_days")))).strftime("%d %B, %Y"),  # noqa
                "num_days": request.POST.get("num_days"),
                "num_guests": request.POST.get("num_guests"),
                "message": request.POST.get("message").replace("\n", "<br>"),
                "destinations": destinations,
            }

            # send multi-part email (plain text and HTML)
            subject = "New Travel Request (Iraqi Kurdistan Guide)"
            from_email = settings.DEFAULT_FROM_EMAIL  # from Developer
            to_email = [settings.DEFAULT_OWNER_EMAIL]  # to Owner
            reply_to_email = request.POST.get("email")
            # bcc_email = [settings.DEFAULT_FROM_EMAIL]  # bcc: Developer

            text_content = render_to_string("contact/emails/trip_request.txt", {"form_context": form_context})  # noqa
            html_content = render_to_string("contact/emails/trip_request.html", {"form_context": form_context})  # noqa

            try:
                email = EmailMultiAlternatives(subject, text_content, from_email, to_email, reply_to=[reply_to_email])  # noqa
                # email = EmailMultiAlternatives(subject, text_content, from_email, to_email, bcc=bcc_email, reply_to=[reply_to_email])  # reply-to and bcc  # noqa
                email.attach_alternative(html_content, "text/html")
                email.send()
                messages.success(
                    request,
                    "Thank You! We'll be in touch with you soon!"
                )
                return redirect(reverse("home"))

            except BadHeaderError:
                messages.error(request, "Error: Invalid Header Found.")
                return redirect(reverse("contact"))

            except Exception as e:
                print(f"Error sending email: {e}")
                messages.error(request, "Error: Please Try Again.")
                return redirect(reverse("contact"))

    template = "contact/contact.html"
    context = {
        "contact_form": contact_form,
    }
    return render(request, template, context)

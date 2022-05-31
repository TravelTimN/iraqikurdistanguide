from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Booking
from .forms import BookingForm


@login_required()
def bookings(request):
    """ A view to return the admin-only Bookings page """
    if not request.user.is_superuser:
        # user is not superuser; take them home
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("home"))
    bookings = Booking.objects.all()
    template = "bookings/bookings.html"
    context = {
        "bookings": bookings,
    }
    return render(request, template, context)


@login_required
def add_booking(request):
    """ A view to add a single booking """
    if not request.user.is_superuser:
        # user is not superuser; take them home
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("home"))
    booking_form = BookingForm(request.POST or None)
    if request.method == "POST":
        if booking_form.is_valid():
            next = request.POST.get("next", "/")
            booking_form.save()
            messages.success(request, "Booking Added!")
            return HttpResponseRedirect(next)
        messages.error(request, "Error: Please Try Again.")
    template = "bookings/add_booking.html"
    context = {
        "booking_form": booking_form,
    }
    return render(request, template, context)


@login_required
def update_booking(request, id):
    """ A view to update a single booking """
    if not request.user.is_superuser:
        # user is not superuser; take them home
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("home"))
    booking = get_object_or_404(Booking, id=id)
    booking_form = BookingForm(request.POST or None, instance=booking)
    if request.method == "POST":
        if booking_form.is_valid():
            next = request.POST.get("next", "/")
            booking_form.save()
            messages.success(request, "Booking Updated!")
            return HttpResponseRedirect(next)
        messages.error(request, "Error: Please Try Again.")
    template = "bookings/update_booking.html"
    context = {
        "booking": booking,
        "booking_form": booking_form,
    }
    return render(request, template, context)


@login_required
def delete_booking(request, id):
    """ A view to delete a specific booking """
    if not request.user.is_superuser:
        # user is not superuser; take them home
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("home"))
    booking = get_object_or_404(Booking, id=id)
    booking.delete()
    messages.success(request, "Booking Deleted!")
    return redirect(reverse("bookings"))

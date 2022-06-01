import calendar
from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Booking
from .forms import BookingForm
from .utils import BookingCalendar


def get_date(d):
    """
        Get the YYYY-M from args
    """
    if d:
        year, month = (int(x) for x in d.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def get_prev_month(d):
    """
        Calculate the previous month from the YYYY-M in args
    """
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def get_next_month(d):
    """
        Calculate the next month from the YYYY-M in args
    """
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


@login_required()
def bookings(request):
    """ A view to return the admin-only Bookings page """
    if not request.user.is_superuser:
        # user is not superuser; take them home
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("home"))
    # get all bookings
    bookings = Booking.objects.all()
    # generate utils.BookingCalendar using month-args
    d = get_date(request.GET.get("month", None))
    calendar = BookingCalendar(d.year, d.month)
    booking_calendar = calendar.formatmonth(withyear=True)
    # define prev/next months
    prev_month = get_prev_month(d)
    next_month = get_next_month(d)
    template = "bookings/bookings.html"
    context = {
        "bookings": bookings,
        "prev_month": prev_month,
        "next_month": next_month,
        "booking_calendar": booking_calendar,
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

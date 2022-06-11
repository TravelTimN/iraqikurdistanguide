import calendar
from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from .models import Booking
from .forms import BookingForm
from .utils import BookingCalendar
from main.decorators import validate_user


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


@validate_user()
def bookings(request):
    """ A view to return the admin-only Bookings page """
    # generate utils.BookingCalendar using month-args
    d = get_date(request.GET.get("month", None))
    calendar = BookingCalendar(d.year, d.month)
    booking_calendar = calendar.formatmonth(withyear=True)
    # define prev/next months
    prev_month = get_prev_month(d)
    next_month = get_next_month(d)
    # get all bookings filtered by start/end, according to current Calendar view
    bookings = Booking.objects.filter(
        (Q(start_date__month=d.month) | Q(start_date__month__lt=d.month) | Q(start_date__year__lt=d.year)) &
        (Q(end_date__month=d.month) | Q(end_date__month__gt=d.month) | Q(end_date__year__gt=d.year)) &
        (Q(start_date__year=d.year) | Q(end_date__year__gte=d.year))
    )
    template = "bookings/bookings.html"
    context = {
        "bookings": bookings,
        "prev_month": prev_month,
        "next_month": next_month,
        "booking_calendar": booking_calendar,
    }
    return render(request, template, context)


@validate_user()
def add_booking(request):
    """ A view to add a single booking """
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


@validate_user()
def update_booking(request, id):
    """ A view to update a single booking """
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


@validate_user()
def delete_booking(request, id):
    """ A view to delete a specific booking """
    booking = get_object_or_404(Booking, id=id)
    booking.delete()
    messages.success(request, "Booking Deleted!")
    return redirect(reverse("bookings"))

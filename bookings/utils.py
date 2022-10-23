import calendar
from datetime import datetime
from django.db.models import Q
from .models import Booking


class BookingCalendar(calendar.HTMLCalendar):
    # calendar setup: https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
    # calendar responsiveness: https://codepen.io/chrisdpratt/pen/OOybam
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(BookingCalendar, self).__init__()

    # filter bookings by day
    def formatday(self, day, weekday, month, year, bookings):
        # add booking to every day that a guest's trip exists
        bookings_per_day = bookings.filter(
            (Q(start_date__day__lte=day) | Q(start_date__month__lt=month) | Q(start_date__year__lt=year)) &
            (Q(end_date__day__gte=day) | Q(end_date__month__gt=month) | Q(end_date__year__gt=year)) &
            (Q(start_date__year=year) | Q(end_date__year__gte=year))
        )

        d = ""
        for booking in bookings_per_day:
            # truncate longer guest names
            guest = (booking.guest_name[:15] + "..") if len(booking.guest_name) > 15 else booking.guest_name
            d += f"<a href='#' class='d-block py-1 px-2 w-100 mb-1 rounded text-truncate small bg-success text-white' data-bs-toggle='modal' data-bs-target='#modal{booking.id}'>{guest}</a>"

        if day != 0:
            # if the day of month is "today", this year specifically
            if day == datetime.now().day and month == datetime.now().month and year == datetime.now().year:
                return f"""
                <div class="col-md day p-2 bg-warning bg-opacity-25 text-truncate">
                    <p class="row align-items-center fs-4">
                        <span class="date col-1">{day}</span>
                        <small class="col d-md-none text-center">{calendar.day_name[weekday]}</small>
                        <span class="col-1"></span>
                    </p>
                    <p class="d-md-none text-danger">No Bookings</p>
                    {d}
                </div>
                """

            if d:
                # part of the current month, and has at least one existing booking
                return f"""
                <div class="col-md day p-2 border border-left-0 border-top-0 text-truncate">
                    <p class="row align-items-center fs-4">
                        <span class="date col-1">{day}</span>
                        <small class="col d-md-none text-center">{calendar.day_name[weekday]}</small>
                        <span class="col-1"></span>
                    </p>
                    {d}
                </div>
                """
            else:
                # part of the current month, but has 0 bookings
                return f"""
                <div class="col-md day p-2 border border-left-0 border-top-0 text-truncate d-none d-md-inline-block">
                    <p class="row align-items-center fs-4">
                        <span class="date col-1">{day}</span>
                        <small class="col d-md-none text-center">{calendar.day_name[weekday]}</small>
                        <span class="col-1"></span>
                    </p>
                    <p class="d-md-none">No Bookings</p>
                </div>
                """

        # days that bleed from/to a different month
        return f"""
        <div class="col-md day p-2 border border-left-0 border-top-0 text-truncate d-none d-md-inline-block bg-light text-muted">
            <p class="row align-items-center fs-4">
                <span class="date col-1"></span>
                <small class="col d-md-none text-center text-muted"></small>
                <span class="col-1"></span>
            </p>
            <p class="d-md-none">No Bookings</p>
        </div>
        """

    # formats a week as individual row
    def formatweek(self, theweek, bookings, month, year):
        week = ""
        # loop day/weekday to generate each daily booking event
        for d, weekday in theweek:
            week += self.formatday(d, weekday, month, year, bookings)
        # must have .w-100 div after each week to force new-line
        return f"{week}<div class='w-100'></div>"

    # filter bookings by year/month
    def formatmonth(self, withyear=True):
        bookings = Booking.objects.filter(
            Q(start_date__year=self.year, start_date__month=self.month) |
            Q(start_date__month__lt=self.month, end_date__month=self.month) |
            Q(start_date__year__lt=self.year, end_date__month=self.month)
        )
        # build the month/year header
        booking_calendar = f"""<header>
            <h4 id="calendar-header" class="display-4 text-center">{calendar.month_name[self.month]} {self.year}</h4>
            <div class="row d-none d-md-flex p-1 bg-dark text-white">
        """
        # loop days of week header
        wk = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        for w in wk:
            booking_calendar += f"<h5 class='col-md px-1 py-0 m-0 lh-base text-center'>{w}</h5>"
        booking_calendar += """</div>
        </header>
        <div class="row border border-right-0 border-bottom-0">
        """
        # loop each week and append to the calendar
        for week in self.monthdays2calendar(self.year, self.month):
            booking_calendar += f"{self.formatweek(week, bookings, self.month, self.year)}\n"
        booking_calendar += "</div>"
        return booking_calendar

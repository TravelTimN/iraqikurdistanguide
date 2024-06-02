from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import Itinerary, ItineraryDay
from .forms import ItineraryForm, ItineraryDayForm
from main.decorators import validate_user


# --- ALL ITINERARIES --- #
def itineraries(request):
    """ A view to return the Itineraries page """
    if request.user.groups.filter(name="Site Admin"):
        itineraries = Itinerary.objects.all().prefetch_related("days__destinations", "days__overnight_city__province").order_by("id")  # noqa
    else:
        itineraries = Itinerary.objects.prefetch_related("days__destinations", "days__overnight_city__province").filter(is_visible=True).order_by("id")  # noqa
    template = "itineraries/itineraries.html"
    context = {
        "itineraries": itineraries,
    }
    return render(request, template, context)


# --- ITINERARY --- #
@validate_user()
def add_itinerary(request):
    """ A view to add a new Itinerary """
    itinerary_form = ItineraryForm(request.POST or None)
    if request.method == "POST":
        if itinerary_form.is_valid():
            itinerary = itinerary_form.save()
            messages.success(request, "Itinerary Added!")
            return redirect(add_itinerary_day, itinerary.pk)
    template = "itineraries/add_itinerary.html"
    context = {
        "itinerary_form": itinerary_form,
    }
    return render(request, template, context)


@validate_user()
def update_itinerary(request, id):
    """ A view to update a specific Itinerary """
    itinerary = get_object_or_404(Itinerary, id=id)
    itinerary_form = ItineraryForm(request.POST or None, instance=itinerary)
    if request.method == "POST":
        if itinerary_form.is_valid():
            itinerary_form.save()
            messages.success(request, "Itinerary Updated!")
            return redirect(reverse("itineraries"))
    template = "itineraries/update_itinerary.html"
    context = {
        "itinerary": itinerary,
        "itinerary_form": itinerary_form,
    }
    return render(request, template, context)


@validate_user()
def delete_itinerary(request, id):
    """ A view to delete a specific Itinerary """
    itinerary = get_object_or_404(Itinerary, id=id)
    itinerary.delete()
    messages.success(request, "Itinerary and Days Deleted!")
    return redirect(reverse("itineraries"))


# --- ITINERARY DAYS --- #
@validate_user()
def add_itinerary_day(request, id):
    """ A view to add a new Itinerary Day"""
    itinerary = get_object_or_404(Itinerary, id=id)
    
    # get the next available day number
    last_day = ItineraryDay.objects.filter(itinerary=itinerary).order_by('-day_number').first()  # noqa
    next_day_number = last_day.day_number + 1 if last_day else 1

    itinerary_day_form = ItineraryDayForm(request.POST or None, initial={"day_number": next_day_number})  # noqa
    if request.method == "POST":
        if itinerary_day_form.is_valid():
            itinerary_day = itinerary_day_form.save(commit=False)
            itinerary_day.itinerary = itinerary
            itinerary_day.day_number = next_day_number
            itinerary_day.save()
            itinerary_day_form.save_m2m()  # set M2M "destinations"

            messages.success(request, f"Day {next_day_number} Added!")

            # adding a single day, or continuing with another one afterwards?
            submit_type = request.POST.get("submit_type")
            if submit_type == "multiple":
                # save day then create the next day
                return redirect("add_itinerary_day", id=itinerary.id)
            else:
                # only save the single day
                return redirect(reverse("itineraries"))

        else:
            messages.error(request, "Error: Please try again!")

    template = "itineraries/add_itinerary_day.html"
    context = {
        "itinerary": itinerary,
        "itinerary_day_form": itinerary_day_form,
        "day_number": next_day_number,
    }
    return render(request, template, context)


@validate_user()
def update_itinerary_day(request, itin_id, day_id):
    """ A view to update a specific Itinerary Day """
    itinerary = get_object_or_404(Itinerary, id=itin_id)
    itinerary_day = get_object_or_404(ItineraryDay, id=day_id)
    itinerary_day_form = ItineraryDayForm(request.POST or None, instance=itinerary_day)
    if request.method == "POST":
        if itinerary_day_form.is_valid():
            itinerary_day_form.save()
            messages.success(request, "Itinerary Day Updated!")
            return redirect(reverse("itineraries"))
    template = "itineraries/update_itinerary_day.html"
    context = {
        "itinerary": itinerary,
        "itinerary_day": itinerary_day,
        "day_number": itinerary_day.day_number,
        "itinerary_day_form": itinerary_day_form,
    }
    return render(request, template, context)


# resequence helper function
def resequence_days(id):
    """
    Resequence the day_number for an itinerary's days
    after deletion of a specific day.
    Eg: Itinerary Foobar has 10 days. Day 4 gets deleted.
    Resequence its days to avoid gaps.
    """
    itinerary_days = ItineraryDay.objects.filter(itinerary_id=id).order_by("day_number")  # noqa
    for index, day in enumerate(itinerary_days):
        day.day_number = index + 1
        day.save()


@validate_user()
def delete_itinerary_day(request, itin_id, day_id):
    """ A view to delete a specific Itinerary Day """
    itinerary_day = get_object_or_404(ItineraryDay, id=day_id)
    itinerary_day.delete()
    messages.success(request, "Itinerary Day Deleted!")
    # resequence Itinerary's remaining days to avoid gaps
    resequence_days(itin_id)
    return redirect(reverse("itineraries"))

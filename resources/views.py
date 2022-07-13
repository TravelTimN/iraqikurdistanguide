from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Phrase
from .forms import PhraseForm
from main.decorators import validate_user


def resources(request):
    """ A view to return the resources page """
    template = "resources/resources.html"
    context = {}
    return render(request, template, context)


def alphabet(request):
    """ A view to return the alphabet page """
    template = "resources/alphabet.html"
    return render(request, template)


def entertainment(request):
    """ A view to return the entertainment page """
    template = "resources/entertainment.html"
    return render(request, template)


def holidays(request):
    """ A view to return the holidays page """
    template = "resources/holidays.html"
    return render(request, template)


def phrases(request):
    """ A view to return the phrases page """
    if request.user.is_superuser:
        phrases = Phrase.objects.all().order_by("category")
    else:
        phrases = Phrase.objects.filter(is_visible=True).order_by("category")
    template = "resources/phrases.html"
    context = {
        "phrases": phrases,
    }
    return render(request, template, context)


@validate_user()
def add_phrase(request):
    """ A view to add a single phrase """
    phrase_form = PhraseForm(request.POST or None)
    if request.method == "POST":
        if phrase_form.is_valid():
            next = request.POST.get("next", "/")
            new_phrase = phrase_form.save()
            messages.success(request, "New Phrase Added!")
            return HttpResponseRedirect(next)
        messages.error(request, "Error: Please Try Again.")
    template = "resources/add_phrase.html"
    context = {
        "phrase_form": phrase_form,
    }
    return render(request, template, context)


@validate_user()
def update_phrase(request, id):
    """ A view to update a single phrase """
    phrase = get_object_or_404(Phrase, id=id)
    phrase_form = PhraseForm(request.POST or None, instance=phrase)
    if request.method == "POST":
        if phrase_form.is_valid():
            next = request.POST.get("next", "/")
            phrase_form.save()
            messages.success(request, "Phrase Updated!")
            return HttpResponseRedirect(next)
        messages.error(request, "Error: Please Try Again.")
    template = "resources/update_phrase.html"
    context = {
        "phrase": phrase,
        "phrase_form": phrase_form,
    }
    return render(request, template, context)


@validate_user()
def delete_phrase(request, id):
    """ A view to delete a specific phrase """
    phrase = get_object_or_404(Phrase, id=id)
    phrase.delete()
    messages.success(request, "Phrase Deleted!")
    return redirect(reverse("phrases"))


def weather(request):
    """ A view to return the weather page """
    template = "resources/weather.html"
    return render(request, template)

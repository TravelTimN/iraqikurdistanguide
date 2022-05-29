from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Phrase
from .forms import PhraseForm


def resources(request):
    """ A view to return the resources page """
    template = "resources/resources.html"
    context = {}
    return render(request, template, context)


def alphabet(request):
    """ A view to return the alphabet page """
    template = "resources/alphabet.html"
    context = {}
    return render(request, template, context)


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


@login_required
def add_phrase(request):
    """ A view to add a single phrase """
    if not request.user.is_superuser:
        # user is not superuser; take them to all phrases
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("phrases"))
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


@login_required
def update_phrase(request, id):
    """ A view to update a single phrase """
    if not request.user.is_superuser:
        # user is not superuser; take them to all phrases
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("phrases"))
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


@login_required
def delete_phrase(request, id):
    """ A view to delete a specific phrase """
    if not request.user.is_superuser:
        # user is not superuser; take them to all phrases
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("phrases"))
    phrase = get_object_or_404(Phrase, id=id)
    phrase.delete()
    messages.success(request, "Phrase Deleted!")
    return redirect(reverse("phrases"))

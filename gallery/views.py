from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Photo
from .forms import PhotoForm
from main.decorators import validate_user


def gallery(request):
    """ A view to return the gallery page """
    if request.user.groups.filter(name="Site Admin"):
        photos = Photo.objects.all().order_by("sight__destination")
    else:
        photos = Photo.objects.filter(is_visible=True).order_by("sight__destination")
    template = "gallery/gallery.html"
    context = {
        "photos": photos,
    }
    return render(request, template, context)


@validate_user()
def add_photo(request):
    """ A view to add a single photo """
    photo_form = PhotoForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if photo_form.is_valid():
            next = request.POST.get("next", "/")
            photo_form.save()
            messages.success(request, "Photo Added!")
            return HttpResponseRedirect(next)
        messages.error(request, "Error: Please Try Again.")
    template = "gallery/add_photo.html"
    context = {
        "photo_form": photo_form,
    }
    return render(request, template, context)


@validate_user()
def update_photo(request, id):
    """ A view to update a single photo """
    photo = get_object_or_404(Photo, id=id)
    photo_form = PhotoForm(request.POST or None, request.FILES or None, instance=photo)
    if request.method == "POST":
        if photo_form.is_valid():
            next = request.POST.get("next", "/")
            photo_form.save()
            messages.success(request, "Photo Updated!")
            return HttpResponseRedirect(next)
        messages.error(request, "Error: Please Try Again.")
    template = "gallery/update_photo.html"
    context = {
        "photo": photo,
        "photo_form": photo_form,
    }
    return render(request, template, context)


@validate_user()
def delete_photo(request, id):
    """ A view to delete a specific photo """
    photo = get_object_or_404(Photo, id=id)
    photo.delete()
    messages.success(request, "Photo Deleted!")
    return redirect(reverse("gallery"))

from django.shortcuts import render


def gallery(request):
    """ A view to return the gallery page """
    return render(request, "gallery/gallery.html")


def add_image(request):
    """ A view to add a single image """
    return render(request, "gallery/add_image.html")


def update_image(request):
    """ A view to update a specific image """
    return render(request, "gallery/update_image.html")

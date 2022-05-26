from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review


def reviews(request):
    """ A view to return the reviews page """
    if request.user.is_superuser:
        reviews = Review.objects.all().order_by("date", "rating")
    else:
        reviews = Review.objects.filter(is_visible=True).order_by("date", "rating")
    template = "reviews/reviews.html"
    context = {
        "reviews": reviews,
    }
    return render(request, template, context)

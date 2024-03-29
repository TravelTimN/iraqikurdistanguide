from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Review
from .forms import ReviewForm
from main.decorators import validate_user



def reviews(request):
    """ A view to return the reviews page """
    if request.user.groups.filter(name="Site Admin"):
        reviews = Review.objects.all().order_by("source", "-date", "-rating")
    else:
        reviews = Review.objects.filter(is_visible=True).order_by("source", "-date", "-rating")
    template = "reviews/reviews.html"
    context = {
        "reviews": reviews,
    }
    return render(request, template, context)


@validate_user()
def add_review(request):
    """ A view to add a single review """
    review_form = ReviewForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if review_form.is_valid():
            next = request.POST.get("next", "/")
            review_form.save()
            messages.success(request, "Review Added!")
            return HttpResponseRedirect(next)
        messages.error(request, "Error: Please Try Again.")
    template = "reviews/add_review.html"
    context = {
        "review_form": review_form,
    }
    return render(request, template, context)


@validate_user()
def update_review(request, id):
    """ A view to update a single review """
    review = get_object_or_404(Review, id=id)
    review_form = ReviewForm(request.POST or None, request.FILES or None, instance=review)
    if request.method == "POST":
        if review_form.is_valid():
            next = request.POST.get("next", "/")
            review_form.save()
            messages.success(request, "Review Updated!")
            return HttpResponseRedirect(next)
        messages.error(request, "Error: Please Try Again.")
    template = "reviews/update_review.html"
    context = {
        "review": review,
        "review_form": review_form,
    }
    return render(request, template, context)


@validate_user()
def delete_review(request, id):
    """ A view to delete a specific review """
    review = get_object_or_404(Review, id=id)
    review.delete()
    messages.success(request, "Review Deleted!")
    return redirect(reverse("reviews"))

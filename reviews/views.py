from django.shortcuts import render


def reviews(request):
    """ A view to return the reviews page """
    return render(request, "reviews/reviews.html")

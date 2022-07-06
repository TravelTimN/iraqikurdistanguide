from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .models import FAQ
from .forms import FAQForm
from main.decorators import validate_user


def faqs(request):
    """ A view to return the FAQs page """
    if request.user.groups.filter(name="Site Admin"):
        faqs = FAQ.objects.all().order_by("category")
    else:
        faqs = FAQ.objects.filter(is_visible=True).order_by("category")
    template = "faqs/faqs.html"
    context = {
        "faqs": faqs,
    }
    return render(request, template, context)


@validate_user()
def add_faq(request):
    """ A view to add a new FAQ """
    faq_form = FAQForm(request.POST or None)
    if request.method == "POST":
        if faq_form.is_valid:
            faq_form.save()
            messages.success(request, "FAQ Added!")
            return redirect(reverse("faqs"))
    template = "faqs/add_faq.html"
    context = {
        "faq_form": faq_form,
    }
    return render(request, template, context)


@validate_user()
def update_faq(request, id):
    """ A view to update a specific FAQ """
    faq = get_object_or_404(FAQ, id=id)
    faq_form = FAQForm(request.POST or None, instance=faq)
    if request.method == "POST":
        if faq_form.is_valid:
            faq_form.save()
            messages.success(request, "FAQ Updated!")
            return redirect(reverse("faqs"))
    template = "faqs/update_faq.html"
    context = {
        "faq": faq,
        "faq_form": faq_form,
    }
    return render(request, template, context)


@validate_user()
def delete_faq(request, id):
    """ A view to delete a specific FAQ """
    faq = get_object_or_404(FAQ, id=id)
    faq.delete()
    messages.success(request, "FAQ Deleted!")
    return redirect(reverse("faqs"))

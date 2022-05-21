from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FAQ
from .forms import FAQForm


def faqs(request):
    """ A view to return the FAQs page """
    if request.user.is_superuser:
        faqs = FAQ.objects.all().order_by("category")
    else:
        faqs = FAQ.objects.filter(is_visible=True).order_by("category")
    template = "faqs/faqs.html"
    context = {
        "faqs": faqs,
    }
    return render(request, template, context)


@login_required
def add_faq(request):
    """ A view to add a new FAQ """
    if not request.user.is_superuser:
        # user is not superuser; take them to FAQs
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("faqs"))
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


@login_required
def update_faq(request, id):
    """ A view to update a specific FAQ """
    if not request.user.is_superuser:
        # user is not superuser; take them to FAQs
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("faqs"))
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


@login_required
def delete_faq(request, id):
    """ A view to delete a specific FAQ """
    if not request.user.is_superuser:
        # user is not superuser; take them to FAQs
        messages.error(request, "Access denied. Invalid permissions.")
        return redirect(reverse("faqs"))
    faq = get_object_or_404(FAQ, id=id)
    faq.delete()
    messages.success(request, "FAQ Deleted!")
    return redirect(reverse("faqs"))

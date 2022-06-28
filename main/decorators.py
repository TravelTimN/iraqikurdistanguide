from functools import wraps
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import reverse, redirect


def validate_user(redirect_url="home", redirect_kwargs={}):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(request, *args, **kwargs):
            authorized = request.user.is_superuser

            if not authorized and redirect_url:
                messages.error(request, "Access denied. Invalid permissions.")
                return redirect(reverse(redirect_url, kwargs=redirect_kwargs))
            elif not authorized:
                raise PermissionDenied("Access denied. Invalid permissions.")

            return view_function(request, *args, **kwargs)

        return wrapped_view

    return decorator

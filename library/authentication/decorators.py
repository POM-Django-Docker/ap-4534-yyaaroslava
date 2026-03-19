from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden


def role_required(*roles):
    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("login")

            if request.user.role not in roles:
                return HttpResponseForbidden("Forbidden")

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
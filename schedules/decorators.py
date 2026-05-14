from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured

from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def rider_required(redirect_url=None):
    def decorator(function):
        if not callable(function):
            raise ImproperlyConfigured("rider_required must be applied to a callable view function.")

        @wraps(function)
        def _wrapped_view(request, *args, **kwargs):
            # Ensure the user is authenticated
            if not request.user.is_authenticated:
                return redirect('login')

            # Ensure the user is a rider
            if not hasattr(request.user, 'profile') or not request.user.profile.isRider:
                if redirect_url:
                    return redirect(redirect_url)
                return HttpResponseForbidden("You do not have permission to access this page.")

            # Proceed to the original view
            return function(request, *args, **kwargs)

        return _wrapped_view
    return decorator

def driver_required(redirect_url=None):
    def decorator(function):
        if not callable(function):
            raise ImproperlyConfigured("driver_required must be applied to a callable view function.")

        @wraps(function)
        def _wrapped_view(request, *args, **kwargs):
            # Ensure the user is authenticated
            if not request.user.is_authenticated:
                return redirect('login')

            # Check if the user is a driver (isRider == False)
            if not hasattr(request.user, 'profile') or request.user.profile.isRider:
                if redirect_url:
                    return redirect(redirect_url)
                return HttpResponseForbidden("You do not have permission to access this page.")

            # Proceed to the original view
            return function(request, *args, **kwargs)

        return _wrapped_view
    return decorator
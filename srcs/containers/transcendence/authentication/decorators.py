from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.shortcuts import redirect

def custom_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.method == 'POST':
                return JsonResponse({'error': 'User not authenticated'}, status=401)
            else:
                return redirect(settings.LOGIN_URL)

        if request.user.is_authenticated and request.user.twofa_submitted and not request.user.twofa_verified:
            if request.method == 'POST':
                return JsonResponse({'error': 'Two-factor authentication not verified'}, status=403)
            else:
                return redirect('/account/redirect/checker')

        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def profile_modify(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_42:
                return HttpResponseRedirect('/profile')
            else:
                return view_func(request, *args, **kwargs)
    return _wrapped_view

def logout_protection(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method == 'POST':
                return JsonResponse({'error': 'User authenticated'}, status=410)
            else:
                return HttpResponseRedirect('/game')

        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view
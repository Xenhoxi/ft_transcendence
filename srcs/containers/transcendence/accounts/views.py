from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode, base64
from base64 import b64encode
from io import BytesIO
from authentication.models import User
from django.urls import reverse
from django.http import JsonResponse
from django_otp.forms import OTPTokenForm
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from authentication.decorators import custom_login_required, logout_protection


@custom_login_required
def redirect_to_2fa_setup(request):
    user = User.objects.get(username=request.user)
    try:
        device = TOTPDevice.objects.get(user=request.user, name='default')
    except MultipleObjectsReturned:
        device = TOTPDevice.objects.filter(user=request.user, name='default').first()
    except ObjectDoesNotExist:
        device = None
        device = TOTPDevice.objects.create(user=request.user, name='default')
    
    if request.method == 'POST':
        form = OTPTokenForm(data=request.POST, user=request.user)
        
        if form.is_valid():
            token = form.cleaned_data['otp_token']
    
            if device and device.verify_token(token):
                user.twofa_submitted = True
                user.twofa_verified = True
                user.save()
                return JsonResponse({'success': True, 'redirect_url': '/game'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid OTP token.'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid form submission.'})
    else:
        form = OTPTokenForm(user=request.user)
    if device:
        qr_code_img = qrcode.make(device.config_url)
        buffer = BytesIO()
        qr_code_img.save(buffer)
        buffer.seek(0)
        encoded_img = b64encode(buffer.read()).decode()
        qr_code_data = f'data:image/png;base64,{encoded_img}'
    else:
        qr_code_data = None
    
    return render(request, 'accounts/setup.html', {'form': form, 'qr_url': qr_code_data})

@logout_protection
def redirect_to_login(request):
    if request.method == 'POST':
        redirect('login_session')
    else:
    	return render(request, 'accounts/login.html')

@custom_login_required
def check_twofa_status(request):
    return JsonResponse({
        'twofa_verified': request.user.twofa_verified,
        'twofa_submitted': request.user.twofa_submitted
    })

def redirect_to_checker(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':    
        try:
            device = TOTPDevice.objects.get(user=user, name='default')
        except MultipleObjectsReturned:
            device = TOTPDevice.objects.filter(user=user, name='default').first()
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'error': 'No Device found.'})
        form = OTPTokenForm(data=request.POST, user=user)
        if form.is_valid():
            token = form.cleaned_data['otp_token']
            if device and device.verify_token(token):
                user.twofa_verified = True
                user.save()
                return JsonResponse({'success': True, 'redirect_url': '/game'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid OTP token.'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid form submission.'})
    else:
        form = OTPTokenForm(user=user)
        return render(request, 'accounts/checker.html', {'form': form})

@login_required
def delete_2fa(request):
    if request.method == 'POST':
        try:
            totp_device = TOTPDevice.objects.get(user=request.user)
            totp_device.delete()
            request.user.twofa_submitted = False  
            request.user.save()
            return JsonResponse({'success': True, 'message': 'Two-Factor Authentication has been removed.'})
        except TOTPDevice.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No TOTP device found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

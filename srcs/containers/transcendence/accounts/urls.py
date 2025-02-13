from django.urls import path
from . import views

urlpatterns = [
    path('redirect/setup/', views.redirect_to_2fa_setup, name='redirect_to_2fa_setup'),
    path('redirect/login/', views.redirect_to_login),
	path('redirect/checker/', views.redirect_to_checker, name='redirect_to_2fa_checker'),
	path('check-twofa-status/',views.check_twofa_status, name='check_twofa_status'),
    path('delete_2fa/', views.delete_2fa, name='delete_2fa'),
]

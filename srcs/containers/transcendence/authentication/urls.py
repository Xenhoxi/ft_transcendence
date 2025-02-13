# authentication/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from authentication import views
from authentication.views import register, start_oauth2_flow, oauth_callback
from django.urls import path
from two_factor.urls import urlpatterns as tf_urls
# from .views import two_factor_login


urlpatterns = [
    path('', views.authentication),
    path('login_session/', views.login_session, name='login_session'),
    path('register_session/', views.register, name='register_session'),
    path('oauth/start/', views.start_oauth2_flow, name='start_oauth2_flow'),
    path('oauth/callback/', views.oauth_callback, name='oauth_callback'),
	# path('fetch_protected_data/',views.fetch_protected_data),
    path('logout_btn/', views.logout_btn),
    path('social/', views.social),
]

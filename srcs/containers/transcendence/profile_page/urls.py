from django.urls import path

from . import views


urlpatterns = [
    path('', views.history),
    path('modify/', views.profile_update, name='profile_modify'),
    path('normal_games/', views.normal_games),
    path('tournament_games/', views.tournament_game),
]
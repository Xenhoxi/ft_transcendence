from django.urls import path

from . import views


urlpatterns = [
    path('', views.game, name='game'),
    path('canvas/', views.canvas),
    path('scripts/', views.scripts),
    path('match_1v1', views.match_1v1),
    path('tournament', views.tournament),
    path('local_match', views.local_match),
    path('tournament/bracket_graph', views.tournament_bracket),
]
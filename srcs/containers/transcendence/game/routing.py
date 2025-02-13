from django.urls import re_path
from .Lobby_Consumer import LobbyConsumer
from .Game_Consumer import GameConsumer
from .Game_AI_Consumer import GameAIConsumer

websocket_urlpatterns = [
    re_path(r"ws/game/game/", LobbyConsumer.as_asgi()),
    re_path(r"ws/game/match/", GameConsumer.as_asgi()),
    re_path(r"ws/game/match_ai/", GameAIConsumer.as_asgi()),
]
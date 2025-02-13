import json
from linecache import updatecache
from pdb import line_prefix
from venv import create

from time import sleep
from uuid import uuid4
from xmlrpc.client import DateTime

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from authentication.models import User
from game.models import GameLobby, TournamentLobby, TournamentHistory
from django.db.models import Q
from datetime import datetime
import math
import time
import asyncio
import redis
from django.core import serializers
from django.core.cache import cache
from time import process_time
from game.PlayerClass import Player
from game.BallClass import Ball
import uuid


class LobbyConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "game_" + self.scope['user'].username
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        user = User.objects.get(username=self.scope['user'])
        user.channel_name = self.channel_name
        user.save()
        self.accept()

    def disconnect(self, close_code):
        user = User.objects.get(username=self.scope['user'])
        user.in_research = False
        user.is_ready = False
        user.save()
        if GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).exists():
            lobby = GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user)).first()
            lobby.delete()
        lobby_queryset = TournamentLobby.objects.filter(Q(P1=user) | Q(P2=user) | Q(P3=user) | Q(P4=user))
        if lobby_queryset:
            lobby = lobby_queryset.first()
            if not user.is_playing:
                self.remove_from_lobby(lobby, user)
                json_data = {'action': 'opponent_change', 'mode': 'matchmaking_1v1',
                             'players': self.create_json_player(lobby)}
                async_to_sync(self.channel_layer.group_send)(lobby.Name, {'type': 'send_info', 'data': json_data})

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            mode = text_data_json['mode']
            if mode == 'match_1v1':
                self.match_1v1(text_data_json)
            elif mode == 'match_tournament':
                self.tournament(text_data_json)
            elif mode == 'match_ai':
                self.ai_match(text_data_json)
        except json.JSONDecodeError:
            print("Received invalid JSON data")


    def find_opponent(self):
        user = User.objects.get(username=self.scope['user'])
        queryset = User.objects.filter(in_research=True).exclude(id=user.id).order_by('id')
        opponent = queryset.first()
        if opponent:
            return opponent.username
        else:
            return None

    def change_in_research(self, new_state, username):
        user = User.objects.get(username=username)
        user.in_research = new_state
        user.save()

    def change_is_playing(self, new_state, username):
        user = User.objects.get(username=username)
        user.is_playing = new_state
        user.save()

    def send_info(self, event):
        data = event['data']
        self.send(text_data=json.dumps(data))

    def check_lobby_existance(self, opponent, user):
        exists = GameLobby.objects.filter(
            (Q(Player1=user) & Q(Player2=opponent)) | (Q(Player1=opponent) & Q(Player2=user))).exists()
        return exists

    def create_lobby(self, opponent_name):
        opponent = User.objects.get(username=opponent_name)
        user = User.objects.get(username=self.scope['user'])
        self.change_in_research(False, opponent.username)
        self.change_in_research(False, user)
        self.change_is_playing(True, opponent.username)
        self.change_is_playing(True, user)
        if not self.check_lobby_existance(opponent, user):
            lobby = GameLobby.objects.create(Player1=user, Player2=opponent,
                                             Name=f"{user.username}_{opponent.username}")
            async_to_sync(self.channel_layer.group_add)(lobby.Name, user.channel_name)
            async_to_sync(self.channel_layer.group_add)(lobby.Name, opponent.channel_name)

    def searching_1v1(self):
        self.change_in_research(True, self.scope['user'])
        json_data = json.dumps({'action': 'searching', 'mode': 'match_1v1'})
        self.send(json_data)
        opponent_name = self.find_opponent()
        if opponent_name is not None:
            opponent = User.objects.get(username=opponent_name)
            json_data = {'action': 'find_opponent', 'mode': 'matchmaking_1v1', 'opponent': opponent_name}
            async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
            json_data_2 = {'action': 'find_opponent', 'mode': 'matchmaking_1v1',
                           'opponent': self.scope['user'].username}
            async_to_sync(self.channel_layer.group_send)("game_" + opponent_name,
                                                         {'type': 'send_info', 'data': json_data_2})
            self.create_lobby(opponent_name)

    def cancel_1v1(self):
        self.change_in_research(False, self.scope['user'])
        json_data = json.dumps({'action': 'cancel', 'mode': 'match_1v1'})
        self.send(json_data)

    def match_1v1(self, json_data):
        if json_data['action'] == 'searching':
            self.searching_1v1()
        elif json_data['action'] == 'cancel':
            self.cancel_1v1()
        elif json_data['action'] == 'player_ready':
            self.check_player()

    def who_is_the_enemy(self, lobby):
        if lobby.Player1 == User.objects.get(username=self.scope['user']):
            return lobby.Player2
        return lobby.Player1

    def set_player(self, player1, player2, lobby_name):
        cache.set(f"{player1.username}_key", {
            'lobby_name': lobby_name,
            'name': player1.username,
            'x': 0,
            'y': (1080 - 233) / 2,
            'id': 1,
            'up_pressed': False, 'down_pressed': False,
            'game_loop': True
        })
        cache.set(f"{player2.username}_key", {
            'lobby_name': lobby_name,
            'name': player2.username,
            'x': 2040 - 77,
            'y': (1080 - 233) / 2,
            'id': 2,
            'up_pressed': False, 'down_pressed': False,
            'game_loop': False
        })


    def init_pos(self, lobby):
        user = User.objects.get(username=self.scope['user'])
        opponent = self.who_is_the_enemy(lobby)
        if lobby.Player1 == user:
            self.set_player(user, opponent, lobby.Name)
        else:
            self.set_player(opponent, user, lobby.Name)
        cache.set(f"{lobby.Name}_key", {
            'is_game_loop': False,
            'is_tournament': 0,
            'test': False,
            'user_key': f"{user.username}",
            'opponent_key': f"{opponent.username}",
            'posX': (2040 - 30) / 2,
            'posY': (1080 - 30) / 2,
            'speed': 500,
            'dirX': 500,
            'dirY': 0
        })

    def json_creator_racket(self, user):
        user_cache = cache.get(f"{user.username}_key")
        racket = {'up_pressed': user_cache['up_pressed'],
                  'down_pressed': user_cache['down_pressed'],
                  'x': user_cache['x'],
                  'y': user_cache['y'],
                  'score': 0,
                  'name': user.username,
                  }
        return racket

    def json_creator_ball(self, lobby):
        ball_cache = cache.get(f"{lobby.Name}_key")
        ball = {'posX': ball_cache['posX'], 'posY': ball_cache['posY'],
                'speed': ball_cache['speed'],
                'dirX': ball_cache['dirX'],
                'dirY': ball_cache['dirY']
                }
        return ball

    def check_player(self):
        user = User.objects.get(username=self.scope['user'])
        lobby = GameLobby.objects.filter(Q(Player1=user) | Q(Player2=user))
        if lobby:
            self.init_pos(lobby.first())
            opponent = self.who_is_the_enemy(lobby.get())
            if user.is_playing and opponent.is_playing:
                my_racket = self.json_creator_racket(user)
                opponent_racket = self.json_creator_racket(opponent)
                json_ball = self.json_creator_ball(lobby.first())
                json_data = {'action': 'start_game', 'mode': 'matchmaking_1v1', 'my_racket': my_racket,
                             'opponent': opponent_racket, 'ball': json_ball}
                async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
                json_data_2 = {'action': 'start_game', 'mode': 'matchmaking_1v1', 'my_racket': opponent_racket,
                             'opponent': my_racket, 'ball': json_ball}
                async_to_sync(self.channel_layer.group_send)("game_" + opponent.username, {'type': 'send_info', 'data': json_data_2})
                return
        json_data = {'action': 'cancel_lobby', 'mode': 'matchmaking_1v1'}
        async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})
        return

# Tournament lobby

    def remove_from_lobby(self, lobby, user):
        if lobby.P1 == user:
            lobby.P1 = None
        elif lobby.P2 == user:
            lobby.P2 = None
        elif lobby.P3 == user:
            lobby.P3 = None
        elif lobby.P4 == user:
            lobby.P4 = None
        lobby.player_count -= 1
        lobby.save()
        async_to_sync(self.channel_layer.group_discard)(lobby.Name, self.channel_name)
        if lobby.player_count == 0:
            if lobby.Winner_F1 and lobby.Loser_F1 and lobby.Winner_F2 and lobby.Loser_F2:
                TournamentHistory.objects.create(First=lobby.Winner_F1, Second=lobby.Loser_F1, Third=lobby.Winner_F2, Fourth=lobby.Loser_F2, date=datetime.now().strftime("%Y-%m-%d"))
            lobby.delete()

    def add_to_lobby(self, lobby, user):
        if not lobby.P1:
            lobby.P1 = user
        elif not lobby.P2:
            lobby.P2 = user
        elif not lobby.P3:
            lobby.P3 = user
        elif not lobby.P4:
            lobby.P4 = user
        lobby.player_count += 1
        if lobby.player_count == 4:
            lobby.is_full = True
        lobby.save()

    def create_json_player(self, lobby):
        player1 = None
        player2 = None
        player3 = None
        player4 = None
        if lobby.P1:
            player1 = lobby.P1.username
        if lobby.P2:
            player2 = lobby.P2.username
        if lobby.P3:
            player3 = lobby.P3.username
        if lobby.P4:
            player4 = lobby.P4.username
        players = {'p0': player1, 'p1': player2, 'p2': player3, 'p3': player4}
        return players

    def find_tounament_opponents(self):
        user = User.objects.get(username=self.scope['user'])
        lobby_queryset = TournamentLobby.objects.filter(is_full=False)
        if not lobby_queryset:
            lobby = TournamentLobby.objects.create(P1=user, player_count=1, Name=uuid.uuid4().hex)
            async_to_sync(self.channel_layer.group_add)(lobby.Name, self.channel_name)
        else:
            lobby = lobby_queryset.first()
            self.add_to_lobby(lobby, user)
            async_to_sync(self.channel_layer.group_add)(lobby.Name, self.channel_name)
            json_data = {'action': 'opponent_change', 'mode': 'tournament',
                         'players': self.create_json_player(lobby)}
            async_to_sync(self.channel_layer.group_send)(lobby.Name, {'type': 'send_info', 'data': json_data})
            self.status_tournament(lobby, user)

    def status_tournament(self, lobby, user):
        if lobby.is_full:
            json_data = {'action': 'lobby_full', 'mode': 'tournament',
                         'players': self.create_json_player(lobby)}
            async_to_sync(self.channel_layer.group_send)(lobby.Name, {'type': 'send_info', 'data': json_data})

    def searching_tournament(self):
        self.change_tournament_research(True, self.scope['user'])
        json_data = json.dumps({'action': 'searching', 'mode': 'tournament'})
        self.send(json_data)
        self.find_tounament_opponents()

    def change_tournament_research(self, new_state, username):
        user = User.objects.get(username=username)
        user.tournament_research = new_state
        user.save()

    def cancel_tournament(self):
        user = User.objects.get(username=self.scope['user'])
        self.change_in_research(False, self.scope['user'])
        json_data = json.dumps({'action': 'cancel', 'mode': 'tournament'})
        self.send(json_data)
        lobby_queryset = TournamentLobby.objects.filter(Q(P1=user) | Q(P2=user) | Q(P3=user) | Q(P4=user))
        lobby = lobby_queryset.first()
        self.remove_from_lobby(lobby, user)
        json_data = {'action': 'opponent_change', 'mode': 'tournament',
                     'players': self.create_json_player(lobby)}
        async_to_sync(self.channel_layer.group_send)(lobby.Name, {'type': 'send_info', 'data': json_data})

    def init_pos_tournament(self, lobby, player1, player2, game_number):
        self.set_player(player1, player2, lobby.Name)
        self.set_player(player2, player1, lobby.Name)
        cache.set(f"{lobby.Name}_key", {
            'is_game_loop': False,
            'test': False,
            'is_tournament': game_number,
            'user_key': f"{player1.username}",
            'opponent_key': f"{player2.username}",
            'posX': (2040 - 30) / 2,
            'posY': (1080 - 30) / 2,
            'speed': 500,
            'dirX': 500,
            'dirY': 0
        })

    def create_game_tournament(self, player1, player2, game_number):
        if not self.check_lobby_existance(player1, player2):
            self.change_in_research(False, player1.username)
            self.change_in_research(False, player2.username)
            self.change_is_playing(True, player1.username)
            self.change_is_playing(True, player2.username)
            lobby = GameLobby.objects.create(Player1=player1, Player2=player2,
                                             Name=f"{player1.username}_{player2.username}", is_tournament=game_number)
            self.init_pos_tournament(lobby, player1, player2, game_number)
            async_to_sync(self.channel_layer.group_add)(lobby.Name, player1.channel_name)
            async_to_sync(self.channel_layer.group_add)(lobby.Name, player2.channel_name)
            return lobby
        return None

    def first_game(self, lobby_t, user):
        lobby1 = self.create_game_tournament(lobby_t.P1, lobby_t.P2, 1)
        lobby2 = self.create_game_tournament(lobby_t.P3, lobby_t.P4, 2)
        if not lobby1 or not lobby2:
            return
        lobby_queryset = TournamentLobby.objects.filter(Q(P1=user) | Q(P2=user) | Q(P3=user) | Q(P4=user))
        lobby_t = lobby_queryset.first()
        if lobby_t.P1.is_playing and lobby_t.P2.is_playing and lobby_t.P3.is_playing and lobby_t.P4.is_playing:
            if lobby1:
                self.send_data_game(lobby_t.P1, lobby_t.P2, lobby1)
            if lobby2:
                self.send_data_game(lobby_t.P3, lobby_t.P4, lobby2)
            return
        return

    def second_game(self, lobby_t, user):
        lobby1 = self.create_game_tournament(lobby_t.Winner_SF1, lobby_t.Winner_SF2, 3)
        lobby2 = self.create_game_tournament(lobby_t.Loser_SF1, lobby_t.Loser_SF2, 4)
        if not lobby1 or not lobby2:
            return
        lobby_queryset = TournamentLobby.objects.filter(Q(P1=user) | Q(P2=user) | Q(P3=user) | Q(P4=user))
        lobby_t = lobby_queryset.first()
        if lobby_t.P1.is_playing and lobby_t.P2.is_playing and lobby_t.P3.is_playing and lobby_t.P4.is_playing:
            if lobby1:
                self.send_data_game(lobby_t.Winner_SF1, lobby_t.Winner_SF2, lobby1)
            if lobby2:
                self.send_data_game(lobby_t.Loser_SF1, lobby_t.Loser_SF2, lobby2)
            return
        return

    def check_player_tournament(self):
        user = User.objects.get(username=self.scope['user'])
        lobby_queryset = TournamentLobby.objects.filter(Q(P1=user) | Q(P2=user) | Q(P3=user) | Q(P4=user))
        lobby_t = lobby_queryset.first()
        if lobby_t:
            if lobby_t.game_played == 0:
                self.first_game(lobby_t, user)
            elif lobby_t.game_played == 2:
                self.second_game(lobby_t, user)
        else:
            json_data = {'action': 'cancel_lobby', 'mode': 'match_tournament'}
            async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': json_data})

    def send_data_game(self, player1, player2, lobby):
        my_racket = self.json_creator_racket(player1)
        opponent_racket = self.json_creator_racket(player2)
        json_ball = self.json_creator_ball(lobby)
        json_data = {'action': 'start_game', 'mode': 'matchmaking_1v1', 'my_racket': my_racket,
                     'opponent': opponent_racket, 'ball': json_ball}
        async_to_sync(self.channel_layer.group_send)("game_" + lobby.Player1.username, {'type': 'send_info', 'data': json_data})
        json_data_2 = {'action': 'start_game', 'mode': 'matchmaking_1v1', 'my_racket': opponent_racket,
                       'opponent': my_racket, 'ball': json_ball}
        async_to_sync(self.channel_layer.group_send)("game_" + lobby.Player2.username,
                                                     {'type': 'send_info', 'data': json_data_2})

    def check_second_game(self):
        user = User.objects.get(username=self.scope['user'])
        lobby_queryset = TournamentLobby.objects.filter(Q(P1=user) | Q(P2=user) | Q(P3=user) | Q(P4=user))
        lobby_t = lobby_queryset.first()
        if lobby_t:
            if lobby_t.is_finished:
                self.remove_from_lobby(lobby_t, user)
                return
            if not lobby_t.is_finished and lobby_t.game_played >= 3:
                return
            if lobby_t.is_canceled:
                lobby_t.delete()
                json_data = {'action': 'cancel_lobby', 'mode': 'matchmaking_1v1'}
                async_to_sync(self.channel_layer.group_send)("game_" + lobby_t.P1.username,
                                                             {'type': 'send_info', 'data': json_data})
                async_to_sync(self.channel_layer.group_send)("game_" + lobby_t.P2.username,
                                                             {'type': 'send_info', 'data': json_data})
                async_to_sync(self.channel_layer.group_send)("game_" + lobby_t.P3.username,
                                                             {'type': 'send_info', 'data': json_data})
                async_to_sync(self.channel_layer.group_send)("game_" + lobby_t.P4.username,
                                                             {'type': 'send_info', 'data': json_data})
                return
            json_data = {'action': 'second_match', 'mode': 'matchmaking_1v1'}
            async_to_sync(self.channel_layer.group_send)("game_" + user.username,
                                                         {'type': 'send_info', 'data': json_data})
            user.is_ready = True
            user.save()
            if lobby_t.P1 and lobby_t.P2 and lobby_t.P3 and lobby_t.P4:
                if lobby_t.P1.is_ready and lobby_t.P2.is_ready and lobby_t.P3.is_ready and lobby_t.P4.is_ready:
                    json_data = {'action': 'launch_second_match', 'mode': 'matchmaking_1v1'}
                    async_to_sync(self.channel_layer.group_send)("game_" + lobby_t.P1.username,
                                                                 {'type': 'send_info', 'data': json_data})
                    async_to_sync(self.channel_layer.group_send)("game_" + lobby_t.P2.username,
                                                                 {'type': 'send_info', 'data': json_data})
                    async_to_sync(self.channel_layer.group_send)("game_" + lobby_t.P3.username,
                                                                 {'type': 'send_info', 'data': json_data})
                    async_to_sync(self.channel_layer.group_send)("game_" + lobby_t.P4.username,
                                                                 {'type': 'send_info', 'data': json_data})
                    return
                return
        json_data = {'action': 'no_tournament', 'mode': 'matchmaking_1v1'}
        async_to_sync(self.channel_layer.group_send)("game_" + user.username,
                                                     {'type': 'send_info', 'data': json_data})

    def tournament(self, json_data):
        if json_data['action'] == 'searching':
            self.searching_tournament()
        elif json_data['action'] == 'cancel':
            self.cancel_tournament()
        elif json_data['action'] == 'player_ready':
            self.check_player_tournament()
        elif json_data['action'] == 'is_tournament':
            self.check_second_game()

# AI LOBBY
    def ai_match(self, json_data):
        if json_data['action'] == 'searching':
            json_data = json.dumps({'action': 'searching', 'mode': 'match_ai'})
            self.send(json_data)
            self.searching_ai()
        elif json_data['action'] == 'player_ready':
            self.start_game_ia()

    def searching_ai(self):
        self.change_in_research(False, self.scope['user'])
        json_data = json.dumps({'action': 'find_opponent', 'mode': 'match_ai', 'opponent': 'ai'})
        self.send(json_data)

    def start_game_ia(self):
        user = User.objects.get(username=self.scope['user'])
        self.change_in_research(False, self.scope['user'])
        self.change_is_playing(True, self.scope['user'])
        self.init_ai(user)
        my_racket = self.json_creator_racket(user)
        ai_cache = cache.get(f"{user.username}_ai_key")
        ai_racket = {'up_pressed': ai_cache['up_pressed'],
                     'down_pressed': ai_cache['down_pressed'],
                     'x': ai_cache['x'],
                     'y': ai_cache['y'],
                     'score': 0,
                     'name': 'ai'}
        ball_cache = cache.get(f"{ai_cache['lobby_name']}_key")
        json_ball = {'posX': ball_cache['posX'], 'posY': ball_cache['posY'],
                     'speed': ball_cache['speed'],
                     'dirX': ball_cache['dirX'],
                     'dirY': ball_cache['dirY']}
        json_data = json.dumps({'action': 'start_game', 'mode': 'match_ai',
                                'my_racket': my_racket, 'opponent': ai_racket, 'ball': json_ball})
        self.send(json_data)

    def init_ai(self, user):
        cache.set(f"{user.username}_key", {
            'lobby_name': user.username + "_lobby_ai",
            'name': user.username,
            'x': 0,
            'y': (1080 - 233) / 2,
            'id': 1,
            'up_pressed': False, 'down_pressed': False,
            'game_loop': True
        })
        cache.set(f"{user.username}_ai_key", {
            'lobby_name': user.username + "_lobby_ai",
            'name': 'ai',
            'x': 2040 - 77,
            'y': (1080 - 233) / 2,
            'id': 2,
            'up_pressed': False, 'down_pressed': False,
            'game_loop': False
        })
        cache.set(f"{user.username}_lobby_ai_key", {
            'is_game_loop': False,
            'test': False,
            'user_key': f"{user.username}",
            'ai': f"{user.username}_ai",
            'posX': (2040 - 30) / 2,
            'posY': (1080 - 30) / 2,
            'speed': 500,
            'dirX': 500,
            'dirY': 0
        })


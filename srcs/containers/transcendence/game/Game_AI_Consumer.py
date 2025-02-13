import json
from linecache import updatecache
from time import sleep
from xmlrpc.client import DateTime

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from authentication.models import User
from game.models import GameLobby, GameHistory
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

class GameAIConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = "match_" + self.scope['user'].username
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        user_cache = await sync_to_async(cache.get)(f"{self.scope['user'].username}_key")
        lobby_cache = await sync_to_async(cache.get)(f"{user_cache['lobby_name']}_key")
        opponent_cache = await sync_to_async(cache.get)(f"{lobby_cache['ai']}_key")
        self.user = Player(user_cache['id'], user_cache['name'])
        self.opponent = Player(opponent_cache['id'], opponent_cache['name'])
        self.ball = Ball()
        if not lobby_cache['is_game_loop']:
            lobby_cache['is_game_loop'] = True
            await sync_to_async(cache.set)(f"{user_cache['lobby_name']}_key", lobby_cache)
            self.task = asyncio.create_task(self.game_loop(lobby_cache))
        await self.accept()

    async def disconnect(self, code):
        self.task.cancel()
        user_name = self.scope['user'].username
        user = await sync_to_async(User.objects.get)(username=user_name)
        user.is_playing = False
        await sync_to_async(user.save)()
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        if await sync_to_async(cache.get)(f"{user_name}_key"):
            user_cache = await sync_to_async(cache.get)(f"{user_name}_key")
            lobby_cache = await sync_to_async(cache.get)(f"{user_cache['lobby_name']}_key")
            if lobby_cache:
                lobby_cache['is_game_loop'] = False
                await sync_to_async(cache.set)(f"{user_cache['lobby_name']}_key", lobby_cache)
            await self.send_data(self.user.get_class(), self.opponent.get_class(), 'game_end')
            await self.check_game(self.user.get_class(), self.opponent.get_class(), True)

#utils

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            if text_data_json['action'] == 'move':
                await self.update_cache(text_data_json)
        except json.JSONDecodeError:
            print("Received invalid JSON data")


    async def send_match_info(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))

    async def ft_sleep(self, delay):
        now = time.time()
        while time.time() < (now + delay):
            continue
# game

    async def check_move(self, user_cache):
        if user_cache['up_pressed'] != self.user.up_pressed or user_cache['down_pressed'] != self.user.down_pressed:
            self.user.up_pressed = user_cache['up_pressed']
            self.user.down_pressed = user_cache['down_pressed']
            return False
        if await self.up_down_ai():
            return False
        return True


    async def json_creator_racket(self, user):
        user_cache = await sync_to_async(cache.get)(f"{user.name}_key")
        racket = {'x': user.x, 'y': user.y,
                  'up_pressed': user_cache['up_pressed'],
                  'down_pressed': user_cache['down_pressed'],
                  'score': user.score}
        return racket

    async def json_creator_ball(self):
        ball = {'posX': self.ball.x , 'posY': self.ball.y,
                'dirX': self.ball.dirX,
                'dirY': self.ball.dirY
                }
        return ball

    # GAME LOGIQUE HERE

    async def game_loop(self, lobby_cache):
        try:
            user_name = self.scope['user'].username
            user_cache = await sync_to_async(cache.get)(f"{user_name}_key")
            ia_time = time.time()
            self.start_time = time.time()
            while lobby_cache['is_game_loop']:

                t1 = time.perf_counter()
                lobby_cache, user_cache, opponent_cache, ball_move = await asyncio.gather(
                    sync_to_async(cache.get)(f"{user_cache['lobby_name']}_key"),
                    sync_to_async(cache.get)(f"{user_name}_key"),
                    sync_to_async(cache.get)(f"{lobby_cache['ai']}_key"),
                    self.ball.move(self.user.get_class(), self.opponent.get_class()),
                )

                if time.time() - ia_time > 1:
                    ia_time = time.time()
                    self.ball.ia_ball_snapshot()
                    if self.ball.ia_dirX > 0:
                        await self.tracking_ai(60)

                await self.check_move(user_cache)

                self.user.move(user_cache['up_pressed'], user_cache['down_pressed'])
                self.opponent.move(self.opponent.up_pressed, self.opponent.down_pressed)

                await self.send_data(self.user.get_class(), self.opponent.get_class(), 'game_data')
                if ball_move == 2:
                    if await self.check_game(self.user.get_class(), self.opponent.get_class(), False):
                        break
                await self.ft_sleep(max(0.0, 0.01667 - (time.perf_counter() - t1)))
            await self.endgame(lobby_cache, user_cache, user_name)
        except asyncio.CancelledError:
            pass

    async def endgame(self, lobby_cache, user_cache, user_name):
        await self.send_data(self.user.get_class(), self.opponent.get_class(), 'game_end')
        await sync_to_async(cache.delete)(f"{lobby_cache['ai']}_key")
        await sync_to_async(cache.delete)(f"{user_cache['lobby_name']}_key")
        await sync_to_async(cache.delete)(f"{user_name}_key")


    async def check_game(self, user, opponent, ff):
        if user.score >= 5 or opponent.score >= 5:
            self.endtime = time.time() - self.start_time
            user = await sync_to_async(User.objects.get)(username=user.name)
            await sync_to_async(GameHistory.objects.create)(History1=user, History2=None,
                                                            Score1=self.user.score, Score2=self.opponent.score,
                                                            ffed1=False, ffed2=False,
                                                            date=datetime.now().strftime("%Y-%m-%d"),
                                                            minutes=self.endtime / 60, seconds=self.endtime % 60)
            return True
        else:
            if ff:
                self.endtime = time.time() - self.start_time
                user = await sync_to_async(User.objects.get)(username=user.name)
                await sync_to_async(GameHistory.objects.create)(History1=user, History2=None,
                                                                Score1=self.user.score, Score2=self.opponent.score,
                                                                ffed1=True, ffed2=False,
                                                                date=datetime.now().strftime("%Y-%m-%d"),
                                                                minutes=self.endtime / 60, seconds=self.endtime % 60)
            return False

    async def update_cache(self, json_data):
        user_name = self.scope['user'].username
        user_cache = await sync_to_async(cache.get)(f"{user_name}_key")
        user_cache['up_pressed'] = json_data['racket']['up_pressed']
        user_cache['down_pressed'] = json_data['racket']['down_pressed']
        await sync_to_async(cache.set)(f"{user_name}_key", user_cache)

    async def send_data(self, player1, player2, action):
        user_json, ball_json = await asyncio.gather(self.json_creator_racket(player1), self.json_creator_ball())
        opponent_json = {'up_pressed': self.opponent.up_pressed,
                         'down_pressed': self.opponent.down_pressed,
                         'x': self.opponent.x, 'y': self.opponent.y,
                         'score': self.opponent.score, 'name': 'ai'}
        json_data = {'action': action, 'mode': 'match_ai', 'my_racket': user_json,
                     'opponent': opponent_json, 'ball': ball_json}
        await self.channel_layer.group_send("match_" + player1.name, {'type': 'send_match_info', 'data': json_data})

# AI GAMEPLAY

    async def up_down_ai(self):
        temp_up = self.opponent.up_pressed
        temp_down = self.opponent.down_pressed
        if self.opponent.y + 30 > self.ball.ia_y:
            self.opponent.up_pressed = True
            self.opponent.down_pressed = False
            return True
        elif self.opponent.y + 193 < self.ball.ia_y:
            self.opponent.down_pressed = True
            self.opponent.up_pressed = False
            return True
        else:
            self.opponent.up_pressed = False
            self.opponent.down_pressed = False
        if temp_up != self.opponent.up_pressed or temp_down != self.opponent.down_pressed:
            return True
        return False

    async def recursive_ai(self, move_left):
        while move_left > 0:
            if self.ball.ia_y + (self.ball.ia_dirY * move_left) > 1050 or self.ball.ia_y + (self.ball.ia_dirY * move_left) < 0:
                if self.ball.ia_dirY > 0:
                    diff = 1050 - self.ball.ia_y
                else:
                    diff = self.ball.ia_y
                before_hit = diff / abs(self.ball.ia_dirY)
                move_left = move_left - before_hit

                self.ball.ia_y = self.ball.ia_y + (self.ball.ia_dirY * before_hit)
                self.ball.ia_x = self.ball.ia_x + ((self.ball.ia_dirX * 0.01667) * before_hit)
                self.ball.ia_dirY = self.ball.ia_dirY * -1

            elif self.ball.ia_x + ((self.ball.ia_dirX * 0.01667) * move_left) >= 2040 - 77:
                before_hit = (2040 - self.ball.ia_x) / abs(self.ball.ia_dirX * 0.01667)
                self.ball.ia_y += self.ball.ia_dirY * before_hit
                return
            else:
                self.ball.ia_y += self.ball.ia_dirY * move_left
                return

    async def tracking_ai(self, move_left):
        if self.ball.ia_dirX > 0:
            await self.recursive_ai(move_left)
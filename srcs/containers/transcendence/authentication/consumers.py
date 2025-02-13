import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import User, FriendList, FriendRequest
from django.db.models import Q
from django.core import serializers


class ActiveConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        user = User.objects.get(username=self.scope['user'])
        user.is_connected = True
        user.save()
        self.room_name = "social_" + self.scope['user'].username
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        user = User.objects.get(username=self.user)
        user.is_connected = False
        user.save()
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        if action == 'friend_list':
            self.send_friend_list()
        elif action == 'request_list':
            self.send_request_list()
        elif action == 'pending_list':
            self.send_pending_list()
        elif action == 'friend_request':
            self.create_request(text_data_json['username'])
        elif action == 'remove_friend':
            self.remove_friend(text_data_json['target'])
        elif action == 'accept_friend_request':
            self.accept_request(text_data_json['target'])
        elif action == 'cancel_deny_request':
            self.cancel_deny_request(text_data_json['target'])
        elif action == 'view_profile':
            self.show_profile(text_data_json['target'])
        elif action == 'update_name':
            self.user = text_data_json['username']

    def send_friend_list(self):
        user = self.scope['user']
        friends = FriendList.objects.filter(Q(user1=user) | Q(user2=user))
        my_friend_list = {'action': 'friend_list', 'friend_list': {'friends': {}}}
        for friend in friends:
            friend_user = friend.user1 if friend.user1 != user else friend.user2
            my_friend_list['friend_list']['friends'][friend_user.username] = {'is_connected': friend_user.is_connected, 'is_playing': friend_user.is_playing}
        json_data = json.dumps(my_friend_list)
        self.send(json_data)

    def send_request_list(self):
        user = self.scope['user']
        recipient = FriendRequest.objects.filter(recipient=user)
        my_recipient_list = {'action': 'request_list', 'request_list': {'request': {}}}
        for receiver in recipient:
            recipient_user = User.objects.filter(username=receiver.requester.username).get()
            my_recipient_list['request_list']['request'][recipient_user.username] = {
                'is_connected': recipient_user.is_connected}
        json_data = json.dumps(my_recipient_list)
        self.send(json_data)

    def send_pending_list(self):
        user = self.scope['user']
        requested = FriendRequest.objects.filter(requester=user)
        my_request_list = {'action': 'pending_list', 'pending_list': {'pending': {}}}
        for request in requested:
            requested_user = User.objects.filter(username=request.recipient.username).get()
            my_request_list['pending_list']['pending'][requested_user.username] = {
                'is_connected': requested_user.is_connected}
        json_data = json.dumps(my_request_list)
        self.send(json_data)

    def create_request(self, target_name):
        requester = self.scope['user']
        if User.objects.filter(username=target_name).exists():
            recipient = User.objects.filter(username=target_name).get()
            info = {'action': 'create_request', 'target': target_name, 'is_connected': recipient.is_connected, 'who': 'pending'}
            info_me = {'action': 'create_request', 'target': requester.username, 'is_connected': requester.is_connected, 'who': 'requester'}
            if requester == recipient:
                error = {'action': 'error',
                         'error': "Error: Cannot add yourself as friend !"}
                self.send(json.dumps(error))
                return
            if not FriendList.objects.filter((Q(user1=requester) & Q(user2=recipient)) | (Q(user1=recipient) & Q(user2=requester))).exists():
                if not FriendRequest.objects.filter((Q(requester=requester) & Q(recipient=recipient)) | (Q(requester=recipient) & Q(recipient=requester))).exists():
                    FriendRequest.objects.create(requester=requester, recipient=recipient)
                    async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': info})
                    async_to_sync(self.channel_layer.group_send)("social_" + target_name, {'type': 'send_info', 'data': info_me})
                else:
                    error = {'action': 'error', 'error': "Error: Friend request already exist (Check pending or request list)!"}
                    self.send(json.dumps(error))
            else:
                error = {'action': 'error', 'error': "Error: User is already your friend !"}
                self.send(json.dumps(error))
        else:
            error = {'action': 'error', 'error': "Error: User not found !"}
            self.send(json.dumps(error))

    def send_info(self, event):
        data = event['data']
        self.send(text_data=json.dumps(data))

    def remove_friend(self, target_name):
        if User.objects.filter(username=target_name).exists():
            target = User.objects.filter(username=target_name).get()
            me = self.scope['user']
            info = {'action': 'remove_friend', 'target': target_name}
            info_me = {'action': 'remove_friend', 'target': me.username}
            if FriendList.objects.filter(user1=me, user2=target).exists():
                FriendList.objects.filter(user1=me, user2=target).delete()
            elif FriendList.objects.filter(user1=target, user2=me).exists():
                FriendList.objects.filter(user1=target, user2=me).delete()
            async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': info})
            async_to_sync(self.channel_layer.group_send)("social_" + target_name, { 'type': 'send_info', 'data': info_me })
        else:
            error = {'action': 'error', 'error': "Error !"}
            self.send(json.dumps(error))

    def accept_request(self, target_name):
        if User.objects.filter(username=target_name).exists():
            target = User.objects.filter(username=target_name).get()
            me = self.scope['user']
            info = {'action': 'accept_friend_request', 'target': target_name, 'is_connected': target.is_connected }
            info_me = {'action': 'accept_friend_request', 'target': me.username, 'is_connected': me.is_connected}
            if not FriendList.objects.filter((Q(user1=me) & Q(user2=target)) | (Q(user1=target) & Q(user2=me))).exists():
                FriendList.objects.create(user1=me, user2=target)
                FriendRequest.objects.filter(requester=target, recipient=me).delete()
            async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': info})
            async_to_sync(self.channel_layer.group_send)("social_" + target_name, {'type': 'send_info', 'data': info_me})
        else:
            error = {'action': 'error', 'error': "Error !"}
            self.send(json.dumps(error))

    def cancel_deny_request(self, target_name):
        if User.objects.filter(username=target_name).exists():
            target = User.objects.filter(username=target_name).get()
            me = self.scope['user']
            info = {'action': 'cancel_deny_request', 'target': target_name}
            info_me = {'action': 'cancel_deny_request', 'target': me.username}
            if FriendRequest.objects.filter(requester=target, recipient=me).exists():
                FriendRequest.objects.filter(requester=target, recipient=me).delete()
            elif FriendRequest.objects.filter(requester=me, recipient=target).exists():
                FriendRequest.objects.filter(requester=me, recipient=target).delete()
            async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': info})
            async_to_sync(self.channel_layer.group_send)("social_" + target_name, {'type': 'send_info', 'data': info_me})
        else:
            error = {'action': 'error', 'error': "Error !"}
            self.send(json.dumps(error))

    def show_profile(self,  target_name):
        info = {'action': 'view_profile', 'target': target_name}
        async_to_sync(self.channel_layer.group_send)(self.room_name, {'type': 'send_info', 'data': info})
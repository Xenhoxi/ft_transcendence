from datetime import datetime
from email.policy import default

from math import trunc

from django.db import models
from django.conf import settings
from authentication.models import User
from django.utils.timezone import now


class GameHistory(models.Model):
    History1 = models.ForeignKey(User, related_name='History1', on_delete=models.CASCADE,  blank=True, null=True)
    History2 = models.ForeignKey(User, related_name='History2', on_delete=models.CASCADE,  blank=True, null=True)
    Score1 = models.IntegerField()
    Score2 = models.IntegerField()
    ffed1 = models.BooleanField(default=False)
    ffed2 = models.BooleanField(default=False)
    date = models.DateField()
    minutes =  models.IntegerField()
    seconds = models.IntegerField()

    def __str__(self):
        return f"{self.History1} - {self.History2}"

class TournamentHistory(models.Model):
    First = models.CharField()
    Second = models.CharField()
    Third = models.CharField()
    Fourth = models.CharField()
    date = models.DateField()

    def __str__(self):
        return f"{self.First} - {self.Second} - {self.Third} - {self.Fourth}"

class GameLobby(models.Model):
    Player1 = models.ForeignKey(User, related_name='Player1', on_delete=models.CASCADE,  blank=True, null=True)
    Player2 = models.ForeignKey(User, related_name='Player2', on_delete=models.CASCADE,  blank=True, null=True)
    Name = models.CharField(blank=True)
    is_tournament = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.Player1.username} - {self.Player2.username}"

class TournamentLobby(models.Model):
    P1 = models.ForeignKey(User, related_name='P1', on_delete=models.CASCADE,  blank=True, null=True)
    P2 = models.ForeignKey(User, related_name='P2', on_delete=models.CASCADE,  blank=True, null=True)
    P3 = models.ForeignKey(User, related_name='P3', on_delete=models.CASCADE,  blank=True, null=True)
    P4 = models.ForeignKey(User, related_name='P4', on_delete=models.CASCADE,  blank=True, null=True)
    Name = models.CharField(blank=True)
    Winner_SF1 = models.ForeignKey(User, related_name='Winner_SF1', on_delete=models.CASCADE,  blank=True, null=True)
    Winner_SF2 = models.ForeignKey(User, related_name='Winner_SF2', on_delete=models.CASCADE,  blank=True, null=True)
    Loser_SF1 = models.ForeignKey(User, related_name='Loser_SF1', on_delete=models.CASCADE,  blank=True, null=True)
    Loser_SF2 = models.ForeignKey(User, related_name='Loser_SF2', on_delete=models.CASCADE,  blank=True, null=True)
    Winner_F1 = models.CharField()
    Winner_F2 = models.CharField()
    Loser_F1 = models.CharField()
    Loser_F2 = models.CharField()
    is_full = models.BooleanField(default=False)
    player_count = models.IntegerField(default=0)
    game_played = models.IntegerField(default=0)
    is_canceled = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Name}"


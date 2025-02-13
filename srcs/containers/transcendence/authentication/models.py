from distutils.command.check import check
from wsgiref.validate import validator

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class User(AbstractUser):
    profile_picture_url = models.URLField(blank=True, null=True)  # Store external URL
    profile_picture = models.ImageField(upload_to='', default='images/Joever.jpg')
    is_connected = models.BooleanField(default=False)
    is_42 = models.BooleanField(default=False)
    is_playing = models.BooleanField(default=False)
    in_research = models.BooleanField(default=False)
    is_ready = models.BooleanField(default=False)
    is_ff = models.BooleanField(default=False)
    tournament_research = models.BooleanField(default=False)
    channel_name = models.CharField(blank=True)
    twofa_submitted = models.BooleanField(default=False)
    twofa_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_profile_picture(self):
        if self.profile_picture_url:
            return self.profile_picture_url
        return self.profile_picture.url


class FriendRequest(models.Model):
    requester = models.ForeignKey(User, related_name='requester', on_delete=models.CASCADE, blank=True)
    recipient = models.ForeignKey(User, related_name='recipient', on_delete=models.CASCADE, blank=True)

    class Meta:
        unique_together = ('requester', 'recipient')

    def __str__(self):
        return f"{self.requester.username} - {self.recipient.username}"


class FriendList(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user1', on_delete=models.CASCADE,  blank=True, null=True)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user2', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.user1.username}"



def username_validator(user_name):
    try:
        CheckIntra_validate(user_name)
        UsernameMaxLength_validate(user_name)
        AllNumUsername_validate(user_name)
    except ValidationError as e:
        raise ValidationError(e.message)

def CheckIntra_validate(username):
    if username.find('_intra_42') != -1:
        raise ValidationError('Illegal name', code='illegal name')

def UsernameMaxLength_validate(username):
    if len(username) > 16:
        raise ValidationError('Username too long', code='username length')

def  AllNumUsername_validate(username):
    if username.isnumeric():
        raise ValidationError('Username cannot be all num', code='all num')
    elif not username.isalnum():
        raise ValidationError('Illegal character in Username', code='illegal char')


class RepeatPasswordValidator:
    def validate(self, password, repeat_password,user=None):
        if password != repeat_password:
            raise ValidationError(
                "Passwords do not match. try again.",
                code='password missmatch',
            )


class PasswordNumberValidator:
    def validate(self, password, user=None):
        if password.isalpha():
            raise ValidationError("Password must contain at least one number",
                                  code='password no number')
class CustomMinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("This password is too short. It must contain at least 8 characters."),
                code='password too short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters."
        ) % {'min_length': self.min_length}
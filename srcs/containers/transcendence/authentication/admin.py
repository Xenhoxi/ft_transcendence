from django.contrib import admin

# Register your models here.
# listings/admin.py
from .models import User, FriendList, FriendRequest


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_connected')


class FriendListAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2')


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('requester', 'recipient')


admin.site.register(User, UserAdmin)
admin.site.register(FriendList, FriendListAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)


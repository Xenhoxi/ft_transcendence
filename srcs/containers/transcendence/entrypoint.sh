#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#empty db
python manage.py makemigrations
python manage.py migrate
python manage.py flush --no-input
python manage.py collectstatic --noinput



# Create superuser if it doesn't exist
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py shell -c "
from django.contrib.auth import get_user_model;
from authentication.models import FriendList
from authentication.models import FriendRequest
from game.models import GameHistory, TournamentHistory

User = get_user_model();

# Create superuser if not exists
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    user = User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
else:
    user = User.objects.get(username='$DJANGO_SUPERUSER_USERNAME')

if not User.objects.filter(username='ludo').exists():
    ludo = User.objects.create_user(username='ludo', email='ludo@maildeludo.com', password='fefe')
if not User.objects.filter(username='leon').exists():
    leon = User.objects.create_user(username='leon', email='leon@maildeludo.com', password='caca')
if not User.objects.filter(username='basi').exists():
    basi = User.objects.create_user(username='basi', email='basi@maildeludo.com', password='caca')
if not User.objects.filter(username='anto').exists():
    anto = User.objects.create_user(username='anto', email='anto@maildeludo.com', password='caca')
if not User.objects.filter(username='abel').exists():
    abel = User.objects.create_user(username='abel', email='abel@maildeludo.com', password='caca')
if not User.objects.filter(username='dcandan').exists():
    dcandan = User.objects.create_user(username='dcandan', email='dcandan@maildeludo.com', password='caca')
if not User.objects.filter(username='leon1').exists():
    leon1 = User.objects.create_user(username='leon1', email='leon@maildeludo.com', password='caca')
if not User.objects.filter(username='leon2').exists():
  leon2 = User.objects.create_user(username='leon2', email='leon@maildeludo.com', password='caca')
if not User.objects.filter(username='leon3').exists():
    leon3 = User.objects.create_user(username='leon3', email='leon@maildeludo.com', password='caca')
if not User.objects.filter(username='leon4').exists():
    leon4 = User.objects.create_user(username='leon4', email='leon@maildeludo.com', password='caca')
if not User.objects.filter(username='leon5').exists():
    leon5 = User.objects.create_user(username='leon5', email='leon@maildeludo.com', password='caca')
if not User.objects.filter(username='leon6').exists():
    leon6 = User.objects.create_user(username='leon6', email='leon@maildeludo.com', password='caca')
if not User.objects.filter(username='leon7').exists():
    leon7 = User.objects.create_user(username='leon7', email='leon@maildeludo.com', password='caca')
if not User.objects.filter(username='leon8').exists():
    leon8 = User.objects.create_user(username='leon8', email='leon@maildeludo.com', password='caca')


if not FriendRequest.objects.filter(requester=leon, recipient=ludo):
    FriendRequest.objects.create(requester=leon, recipient=ludo)
if not FriendRequest.objects.filter(requester=leon, recipient=dcandan):
    FriendRequest.objects.create(requester=leon, recipient=dcandan)
#if not FriendList.objects.filter(user1=leon, user2=ludo).exists():
#    FriendList.objects.create(user1=leon, user2=ludo)
if not FriendList.objects.filter(user1=leon, user2=abel).exists():
    FriendList.objects.create(user1=leon, user2=abel)
if not FriendList.objects.filter(user1=ludo, user2=dcandan).exists():
    FriendList.objects.create(user1=ludo, user2=dcandan)
if not FriendRequest.objects.filter(requester=leon, recipient=ludo):
    FriendRequest.objects.create(requester=leon, recipient=ludo)

TournamentHistory.objects.create(First='dcandan', Second='leon', Third='leon1', Fourth=leon2, date='2024-10-21')
"
fi

exec "$@"
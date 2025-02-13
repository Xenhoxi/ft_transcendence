#!/bin/bash
set -e

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
if not User.objects.filter(username='ludo').exists():
    ludo = User.objects.create_user(username='ludo', email='ludo@maildeludo.com', password='fefe')
"
fi

# Disconnect all users by setting is_connected to False
python manage.py shell -c "
from django.contrib.auth import get_user_model;
from django.contrib.sessions.models import Session;
from django.utils import timezone;

User = get_user_model();
User.objects.all().update(is_connected=False);

# Delete all active sessions to log out users
Session.objects.filter(expire_date__gte=timezone.now()).delete()
"
exec "$@"

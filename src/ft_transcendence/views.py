from django.shortcuts import render


def index(request):
    return render(request, "site/ft_transcendence.html")

from django.shortcuts import render
from authentication.forms import ModifiedProfileForm
from django.http import HttpResponse, JsonResponse
from game.models import GameHistory, TournamentHistory
from django.db.models import Q
from authentication.models import User
from django.contrib.auth.password_validation import validate_password
from authentication.models import username_validator
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from authentication.decorators import custom_login_required, profile_modify


# Create your views here.
@profile_modify
@custom_login_required
def profile_update(request):
    user = User.objects.get(id=request.user.id)
    has_2fa = user.twofa_submitted
    if request.method == 'POST':
        form = ModifiedProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            try:
                if user.profile_picture_url:
                    user.profile_picture_url = ''
                    user.save()
                if form.cleaned_data['username']:
                    username_validator(form.cleaned_data['username'])
                if form.cleaned_data['new_password']:
                    validate_password(form.cleaned_data['new_password'], form.cleaned_data['new_password_repeat'])
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()
                    update_session_auth_hash(request, user)
                    form.save()
                    return JsonResponse({'success':'success', 'username': form.cleaned_data['username'], 'password':'yes'})
                form.save()
                return JsonResponse({'success':'success', 'username': form.cleaned_data['username'], 'password':'no'})
            except ValidationError as e:
                for error in e.error_list:
                    return JsonResponse({'success':'failed', 'error': error.message})
        return JsonResponse({'success':'error'})
    else:
        form = ModifiedProfileForm(instance=user)
    context = {
        'registration_form': form,
        'player': request.user,
        'has_2fa': has_2fa,
    }
    return render(request, 'profile/player_form.html', context)


@custom_login_required
def history(request):
    if request.GET.get('target_name'):
        target_name = request.GET.get('target_name')
        target_user = User.objects.filter(username=target_name).get()
        target = 'friend'
    else:
        target_user = request.user
        target = 'me'
    test = GameHistory.objects.filter(Q(History1=target_user) | Q(History2=target_user))
    five_last_game = list(test)[-20:]
    game_history = []
    for game in reversed(five_last_game):
        if game.History2:
            user2 = {'score': game.Score2, 'username': game.History2.username, 'ff': game.ffed2, 'date': game.date,
                     'time': f"{game.minutes:02}:{game.seconds:02}"}
        else:
            user2 = {'score': game.Score2, 'username': 'IA', 'ff': game.ffed2}
        if game.History1 == target_user:
            game_history.append({
                'User1': {'score': game.Score1, 'username': game.History1.username, 'ff': game.ffed1, 'date': game.date,
                          'time': f"{game.minutes:02}:{game.seconds:02}"},
                'User2': user2
            })
        else:
            game_history.append({
                'User1': user2,
                'User2': {'score': game.Score1, 'username': game.History1.username, 'ff': game.ffed1, 'date': game.date,
                          'time': f"{game.minutes:02}:{game.seconds:02}"}
            })
    context = {
        'target': target,
        'player': target_user,
        'game': game_history
    }
    if target == 'friend':
        return render(request, 'profile/profile_page.html', context)
    else:
        return render(request, 'profile/profile.html', context)

@custom_login_required
def normal_games(request):
    if request.GET.get('target_name'):
        target_name = request.GET.get('target_name')
        target_user = User.objects.filter(username=target_name).get()
        target = 'friend'
    else:
        target_user = request.user
        target = 'me'

    test = GameHistory.objects.filter(Q(History1=target_user) | Q(History2=target_user))
    five_last_game = list(test)[-20:]
    game_history = []
    for game in reversed(five_last_game):
        if game.History2:
            user2 = {'score': game.Score2, 'username': game.History2.username, 'ff': game.ffed2, 'date': game.date,
                     'time': f"{game.minutes:02}:{game.seconds:02}"}
        else:
            user2 = {'score': game.Score2, 'username': 'IA', 'ff': game.ffed2}
        if game.History1 == target_user:
            game_history.append({
                'User1': {'score': game.Score1, 'username': game.History1.username, 'ff': game.ffed1, 'date': game.date,
                          'time': f"{game.minutes:02}:{game.seconds:02}"},
                'User2': user2
            })
        else:
            game_history.append({
                'User1': user2,
                'User2': {'score': game.Score1, 'username': game.History1.username, 'ff': game.ffed1, 'date': game.date,
                          'time': f"{game.minutes:02}:{game.seconds:02}"}
            })
    context = {
        'target': target,
        'player': target_user,
        'game': game_history
    }
    return render(request, 'profile/normal_games.html', context)

@custom_login_required
def tournament_game(request):
    if request.GET.get('target_name'):
        target_name = request.GET.get('target_name')
        target_user = User.objects.filter(username=target_name).get()
        target = 'friend'
    else:
        target_user = request.user
        target = 'me'
    test = TournamentHistory.objects.filter(Q(First=target_user.username) | Q(Second=target_user.username) | Q(Third=target_user.username) | Q(Fourth=target_user.username))
    five_last_game = list(test)[-20:]
    game_history = []
    for game in reversed(five_last_game):
        game_history.append({
            'First': game.First,
            'Second': game.Second,
            'Third': game.Third,
            'Fourth': game.Fourth,
            'date': game.date
        })
    context = {
        'target': target,
        'player': target_user,
        'game': game_history
    }
    return render(request, 'profile/tournament.html', context)



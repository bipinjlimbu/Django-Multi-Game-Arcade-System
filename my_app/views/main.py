from django.shortcuts import render
from ..models import Leaderboard

def home_view(request):
    return render(request, 'main/home_page.html')

def games_view(request):
    return render(request, 'main/games_page.html')

def leaderboard_view(request, game_name):
    if game_name == 'Guess Game':
        players = Leaderboard.objects.filter(game=game_name).order_by('score')
    return render(request, 'main/leaderboard_page.html', {'game_name': game_name, 'players': players})
    